from tronpy import Tron
from tronpy.providers import HTTPProvider

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from dj_rest_auth.registration.serializers import RegisterSerializer

from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import EmailAddress

from rest_framework import serializers

from users.serializers import ReferredUserSerializer

tron = Tron(provider=HTTPProvider(api_key="679bbd65-8f55-4427-86a2-e4a4250be584"))
User = get_user_model()

USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


class CustomRegisterSerializer(RegisterSerializer):
    referral = serializers.CharField(
        max_length=100,
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
    activate_duration = serializers.SerializerMethodField()
    is_active_for_while = serializers.SerializerMethodField()
    total_usage = serializers.SerializerMethodField()
    elapsed = serializers.SerializerMethodField()
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'cm_wallet',
            'referral_code',
            'activate_duration',
            'is_active_for_while',
            'total_usage',
            'elapsed',
            'referred_users',
            'usdt_balance',
            'tron_balance',
        ]

    def get_tron_balance(self, obj):
        return obj.get_tron_balance
    
    def get_usdt_balance(self, obj):
        return obj.get_usdt_balance
    
    def get_activate_duration(self, obj):
        return obj.activate_duration
    
    def get_is_active_for_while(self, obj):
        return obj.is_active_for_while
    
    def get_total_usage(self, obj):
        return obj.calculate_total_usage()
    
    def get_elapsed(self, obj):
        return obj.calculate_elapsed()
    
    def get_referred_users(self, obj):
        referred_users = User.objects.filter(referred_by=obj)
        return ReferredUserSerializer(referred_users, many=True).data
