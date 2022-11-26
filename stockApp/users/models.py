from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserProfile(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=False)
    currency = models.CharField(max_length=255, default='USD')
    premium = models.BooleanField(default=False)
    premium_plan = models.IntegerField()
    companies = models.IntegerField(default=0)
    api_requests = models.IntegerField(default=0)
    api_renewal = models.DateField(default=now)

    def __str__(self):
        return self.owner.username


class Premium(models.Model):
    plan = models.CharField(max_length=255, default='Free')
    company_limit = models.IntegerField()
    api_limit = models.IntegerField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.plan


class Currency(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Currencies'