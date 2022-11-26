from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('generate', csrf_exempt(views.generate_key), name='generate_key'),
    path('deactivate', csrf_exempt(views.deactivate_api), name='deactivate_api'),
    path('documentation', views.documentation, name='api_docs'),
    path('transactions/<api_key>', csrf_exempt(views.transactions_api), name='transactions_api'),
    path('dividends/<api_key>', csrf_exempt(views.dividend_api), name='dividends_api')
]
