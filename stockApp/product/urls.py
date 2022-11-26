from django.urls import path
from. import views
from .views import Product_activation

urlpatterns = [
    path('plan/upgrade', views.index, name='premium'),
    path('plan/confirm/<int:id>', views.confirm, name='confirm'),
    path('plan/payment/<str:order_id>', views.payment_instructions, name='payment'),
    path('product-activation/<uidb64>/<token>', Product_activation.as_view(), name='product_activation')
]