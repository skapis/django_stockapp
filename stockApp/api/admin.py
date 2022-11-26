from django.contrib import admin
from .models import UserAPI


class API(admin.ModelAdmin):
    list_display = ('owner', 'api_key', 'is_active')


admin.site.register(UserAPI, API)
