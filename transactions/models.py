from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    status_choices = [
        ('PENDING', _('Pending')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
        ('FAILED', _('Failed')),
    ]
    status = models.CharField(_("status"), max_length=10, choices=status_choices, default='PENDING')
    requested_at = models.DateTimeField(_("requested at"), auto_now_add=True)
    completed_at = models.DateTimeField(_("completed at"), null=True, blank=True)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return f"Deposit {self.id} - {self.user.email} - {self.status}"

    @property
    def is_completed(self):
        return self.status == 'COMPLETED'

    def complete_deposit(self):
        """Set status to completed and add any logic for completing the deposit."""
        self.status = 'COMPLETED'
        self.completed_at = models.DateTimeField(auto_now=True)
        self.save()

    def cancel_deposit(self):
        """Cancel the deposit if needed."""
        self.status = 'CANCELLED'
        self.save()


class Withdraw(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    status_choices = [
        ('PENDING', _('Pending')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
        ('FAILED', _('Failed')),
    ]
    address = models.CharField(_("wallet address"), max_length=150, blank=True)
    status = models.CharField(_("status"), max_length=10, choices=status_choices, default='PENDING')
    requested_at = models.DateTimeField(_("requested at"), auto_now_add=True)
    completed_at = models.DateTimeField(_("completed at"), null=True, blank=True)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return f"Withdraw {self.id} - {self.user.email} - {self.status}"

    @property
    def is_completed(self):
        return self.status == 'COMPLETED'

    def complete_withdrawal(self):
        """Set status to completed and add any logic for completing the withdrawal."""
        self.status = 'COMPLETED'
        self.completed_at = models.DateTimeField(auto_now=True)
        self.save()

    def cancel_withdrawal(self):
        """Cancel the withdrawal if needed."""
        self.status = 'CANCELLED'
        self.save()
