from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Stock(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    price_date = models.DateField(default=now)
    logo = models.CharField(max_length=255, default='none')
    sector = models.CharField(max_length=255, default='none')
    company_desc = models.CharField(max_length=10000, default='none')
    website = models.CharField(max_length=255, default='none')
    industry = models.CharField(max_length=255, default='none')
    currency = models.CharField(max_length=255, default='none')
    lastDiv = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    exchange = models.CharField(max_length=255, default='none')
    cur_value = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    avg_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)



