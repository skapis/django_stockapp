from django.contrib import admin
from .models import UserProfile, Premium, Currency


class plan(admin.ModelAdmin):
    list_display = ('plan', 'company_limit', 'api_limit', 'price')


class Profile(admin.ModelAdmin):
    list_display = ('owner', 'currency', 'premium', 'premium_plan', 'companies', 'api_requests')


class Currencies(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')


admin.site.register(UserProfile, Profile)
admin.site.register(Premium, plan)
admin.site.register(Currency, Currencies)