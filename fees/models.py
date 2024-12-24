from django.db import models


class Fee(models.Model):
    min_investment = models.IntegerField()
    max_investment = models.IntegerField()
    fee_percentage = models.DecimalField(max_digits=50, decimal_places=2)

    def __str__(self):
        return f"Fee from {self.min_investment} to {self.max_investment} is {self.fee_percentage}%"
