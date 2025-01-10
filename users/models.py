import uuid
from datetime import datetime

from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime, now
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from fees.models import Fee

tron = Tron(provider=HTTPProvider(api_key="679bbd65-8f55-4427-86a2-e4a4250be584"))
USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    wallet = models.CharField(_("wallet address"), max_length=150, blank=True)
    key = models.CharField(_("private key"), max_length=500, blank=True)

    cm_wallet = models.CharField(_("cm wallet address"), max_length=150, blank=True)
    cm_private_key = models.CharField(_("cm private key"), max_length=500, blank=True)
    cm_public_key = models.CharField(_("cm public key"), max_length=500, blank=True)
    cm_hex_address = models.CharField(_("cm hex address"), max_length=150, blank=True)

    profit_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.2)

    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_tron_balance(self):
        try:
            # balance = tron.get_account_balance("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
            balance = tron.get_account_balance(self.cm_wallet)
        except AddressNotFound:
            balance = 0
        return balance
    
    @property
    def get_usdt_balance(self):
        try:
            contract = tron.get_contract(USDT_CONTRACT_ADDRESS)
            # balance = contract.functions.balanceOf("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
            balance = contract.functions.balanceOf(self.cm_wallet)
            balance_in_usdt = balance / (10 ** 6)
        except AddressNotFound:
            balance_in_usdt = 0
        return balance_in_usdt
    
    @property
    def availability(self):
        balance = self.get_usdt_balance

        try:
            fee = Fee.objects.filter(min_investment__lte=balance, max_investment__gte=balance).first()
            return {
                "percent": fee.fee_percentage,
                "duration": fee.hours
            }
        except Exception:
            return {
                "percent": 0,
                "duration": 0
            }
    
    @property
    def is_program_active(self):
        last_usage = self.usage_set.first()

        if not last_usage:
            return True
        
        time_difference = timezone.now() - last_usage.created

        if time_difference.total_seconds() / 3600 < self.availability.get('duration'):
            return False

        return True
    
    def calculate_total_usage(self):
        total_duration = 0
        usages = self.usage_set.all().order_by('created')

        current_time = localtime(now())

        for usage in usages:
            created_time = localtime(usage.created)

            if created_time.date() == current_time.date():
                time_difference = (current_time - created_time).total_seconds() / 3600
            else:
                end_of_day = created_time.replace(hour=24, minute=59, second=59, microsecond=999999)
                time_difference = (end_of_day - created_time).total_seconds() / 3600

            total_duration += min(time_difference, usage.duration)

        return total_duration
    
    def calculate_elapsed(self):
        usage = self.usage_set.first()

        if not usage or usage.created.date() != datetime.today().date():
            return 0
        elapsed = (timezone.now() - usage.created).total_seconds()
        return elapsed
