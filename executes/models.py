from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class Execute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    duration = models.IntegerField(default=0)
    agent_os = models.CharField(max_length=10, null=True, blank=True)  # OS
    http_user_agent = models.CharField(max_length=40, null=True, blank=True)  # HTTP_USER_AGENT
    http_referer = models.CharField(max_length=40, null=True, blank=True)  # HTTP_REFERER
    http_x_forwarded_for = models.CharField(max_length=100, null=True, blank=True) # HTTP_X_FORWARDED_FOR
    profit_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.2)
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Execute from {self.user.email} is ${self.amount}"
    
    def get_profit(self):
        profit = self.amount * self.duration * self.profit_percent / 100
        return profit
    
    def get_platform_fee(self):
        amount = self.get_profit()
        return amount
