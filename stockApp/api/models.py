from django.db import models
from django.contrib.auth.models import User


class UserAPI(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
