from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Fee(models.Model):
    min_investment = models.IntegerField()
    max_investment = models.IntegerField()
    fee_percentage = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return f"Fee from {self.min_investment} to {self.max_investment} is {self.fee_percentage}%"


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investment from {self.user.email} is ${self.amount}"
