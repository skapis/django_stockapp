from django.urls import path
from . import views
from .views import EmailValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'),
    path('select-plan', views.plans, name='plans'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email')
]