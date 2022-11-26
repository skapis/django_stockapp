from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Catalog(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Catalog'

    def __str__(self):
        return self.name


class Users_prod(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=255, default='none')
    is_active = models.BooleanField(default=False)
    active_from = models.DateField()
    active_to = models.DateField()
    payment = models.BooleanField(default=False)
    order_id = models.CharField(max_length=255, default='none')
    order_date = models.DateField(default=now)




