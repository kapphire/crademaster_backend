from django.db import models
from django.contrib.auth import get_user_model

from fees.models import Fee

User = get_user_model()


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investment from {self.user.email} is ${self.amount}"
