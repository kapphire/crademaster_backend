from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.serializers import RegisterSerializer

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import EmailAddress

from rest_framework import serializers

tron = Tron(provider=HTTPProvider(api_key="679bbd65-8f55-4427-86a2-e4a4250be584"))
User = get_user_model()

USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


class CustomRegisterSerializer(RegisterSerializer):
    referral = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )
    cm_wallet = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )
    cm_private_key = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    cm_public_key = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    cm_hex_address = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )

    def get_cleaned_data(self):
        """
        Extend cleaned data to include referral.
        """
        cleaned_data = super().get_cleaned_data()
        cleaned_data['referral'] = self.validated_data.get('referral', '')
        return cleaned_data

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
            
            existing_email = EmailAddress.objects.filter(email=email).first()
            if existing_email and not existing_email.verified:
                existing_email.send_confirmation(self.context.get('request'))
                self.context['resend'] = existing_email.user

            #     raise serializers.ValidationError(
            #         _('This e-mail address is already registered but not verified. '
            #             'A new verification email has been sent to your inbox.')
            #     )
        return email
    
    def custom_signup(self, request, user):
        """
        Custom logic for referral code handling.
        """
        tron_account = tron.generate_address()
        user.cm_wallet = tron_account.get('base58check_address')
        user.cm_private_key = tron_account.get('private_key')
        user.cm_public_key = tron_account.get('public_key')
        user.cm_hex_address = tron_account.get('hex_address')

        referral_code = self.cleaned_data.get('referral')
        if referral_code:
            referred_by = User.objects.filter(referral_code=referral_code).first()
            if referred_by:
                user.referred_by = referred_by
        user.save()

    def save(self, request):
        if self.context.get('resend'):
            return self.context.get('resend')
        return super().save(request)


class CustomUserSerializer(serializers.ModelSerializer):
    usdt_balance = serializers.SerializerMethodField()
    tron_balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'cm_wallet',
            'usdt_balance',
            'tron_balance',
        ]

    def get_tron_balance(self, obj):
        try:
            balance = tron.get_account_balance("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
        except AddressNotFound:
            # raise ValueError("Invalid TRON address or address does not exist")
            balance = 0
        return balance
    
    def get_usdt_balance(self, obj):
        try:
            contract = tron.get_contract(USDT_CONTRACT_ADDRESS)
            balance = contract.functions.balanceOf("THAnMs85N6mcNbKuUbAX826eymbmB7uQs2")
            balance_in_usdt = balance / (10 ** 6)
        except AddressNotFound:
            # raise ValueError("Invalid TRON address or address does not exist")
            balance = 0
        return balance_in_usdt
