import uuid
from datetime import timedelta

from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
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

    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    # last_activated = models.DateTimeField(null=True, blank=True)
    # total_enabled_time = models.DurationField(default=timedelta())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_tron_balance(self):
        try:
            balance = tron.get_account_balance("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
        except AddressNotFound:
            balance = 0
        return balance
    
    @property
    def get_usdt_balance(self):
        try:
            contract = tron.get_contract(USDT_CONTRACT_ADDRESS)
            balance = contract.functions.balanceOf("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
            balance_in_usdt = balance / (10 ** 6)
        except AddressNotFound:
            balance = 0
        return balance_in_usdt
    
    @property
    def activate_duration(self):
        balance = self.get_usdt_balance

        try:
            fee = Fee.objects.filter(min_investment__lte=balance, max_investment__gte=balance).first()
            return fee.hours
        except Fee.DoesNotExist:
            return 0
    
    @property
    def is_active_for_while(self):
        if now() - self.last_activated > self.activate_duration:
            return True
        return False

    def activate(self):
        self.last_activated = now()
        self.save()
