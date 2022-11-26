from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from stocks.models import Stock


class Dividend(models.Model):
    symbol = models.CharField(max_length=255)
    date = models.DateField(default=now)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    stock_id = models.ForeignKey(to=Stock, on_delete=models.CASCADE, default=0)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol

    class Meta:
        ordering = ['-date']