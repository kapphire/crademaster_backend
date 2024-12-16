import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    wallet = models.CharField(_("wallet address"), max_length=150, blank=True)
    key = models.CharField(_("private key"), max_length=500, blank=True)
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')

    is_active_for_hour = models.BooleanField(default=False)
    last_activated = models.DateTimeField(null=True, blank=True)
    total_enabled_time = models.DurationField(default=timedelta())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def activate(self):
        """Activates the user for an hour, ensuring restrictions are met."""
        if self.is_active_for_hour:
            raise ValueError("Already active. Wait for the hour to complete.")
        
        if self.last_activated and (now() - self.last_activated).days < 1:
            raise ValueError("Cannot activate again within a day.")
        
        self.is_active_for_hour = True
        self.last_activated = now()
        self.save()

    def deactivate(self):
        """Deactivates the user after an hour."""
        if not self.is_active_for_hour:
            raise ValueError("User is not currently active.")

        elapsed_time = now() - self.last_activated
        self.total_enabled_time += elapsed_time if elapsed_time < timedelta(hours=1) else timedelta(hours=1)
        self.is_active_for_hour = False
        self.save()


    def reset_activation(self):
        """Check and auto-deactivate after an hour."""
        if self.is_active_for_hour and now() - self.last_activated >= timedelta(hours=1):
            self.deactivate()
