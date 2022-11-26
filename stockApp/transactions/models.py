from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from stocks.models import Stock
import uuid


class Transaction(models.Model):
    symbol = models.CharField(max_length=255)
    cost_share = models.DecimalField(max_digits=9, decimal_places=2)
    shares = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date = models.DateField(default=now)
    broker = models.CharField(max_length=255)
    tr_type = models.CharField(max_length=255)
    stock_id = models.ForeignKey(to=Stock, on_delete=models.CASCADE, default=0)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    fee = models.BooleanField(default=False)
    fee_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.symbol

    class Meta:
        ordering = ['-date']


class Broker(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

