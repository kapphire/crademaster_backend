from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from fees.models import Fee

User = get_user_model()


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investment from {self.user.email} is ${self.amount}"


class Usage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    duration = models.IntegerField(default=0)
    agent_os = models.CharField(max_length=10, null=True, blank=True)  # OS
    http_user_agent = models.CharField(max_length=40, null=True, blank=True)  # HTTP_USER_AGENT
    http_referer = models.CharField(max_length=40, null=True, blank=True)  # HTTP_REFERER
    http_x_forwarded_for = models.CharField(max_length=100, null=True, blank=True) # HTTP_X_FORWARDED_FOR
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Usage from {self.user.email} is ${self.amount}"
