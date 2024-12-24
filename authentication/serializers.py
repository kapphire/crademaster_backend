from tronpy import Tron

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.serializers import RegisterSerializer

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.models import EmailAddress

from rest_framework import serializers

User = get_user_model()
tron = Tron()


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
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
            
            existing_email = EmailAddress.objects.filter(email=email).first()
            if email and existing_email and not existing_email.verified:                
                send_email_confirmation(self.context.get('request'), existing_email.user)
                raise serializers.ValidationError(
                    _('This e-mail address is already registered but not verified. '
                        'A new verification email has been sent to your inbox.')
                )
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
