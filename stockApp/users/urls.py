from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='account'),
    path('edit-account', views.edit_user, name='edit_user'),
    path('change-password', views.change_password, name='change_password'),
    path('change-currency', views.change_currency, name='change_currency'),
]
