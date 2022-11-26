from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='dashboard'),
    path('add-stock', views.add_stock, name='add_stock'),
    path('delete-stock/<int:id>', views.delete_stock, name='delete_stock'),
    path('detail-stock/<int:id>', views.detail_stock, name='detail_stock'),
    path('detail-stock/<int:id>/add', views.add_transaction_from_detail, name='add_transactions_with_id'),
    path('stock-value-summary', csrf_exempt(views.value_by_stock), name='value_by_stock'),
    path('sector-value-summary', csrf_exempt(views.value_by_sector), name='value_by_sector'),
    path('portfolio-performance', csrf_exempt(views.portfolio_performance), name='portfolio_performance'),
    path('check-api', csrf_exempt(views.check_api), name='check-api'),
    path('detail-stock/<int:id>/check-api', csrf_exempt(views.check_api_detail), name='increase-api-detail'),
    path('increase-api', csrf_exempt(views.increase_api), name='check-api'),
    path('detail-stock/<int:id>/increase-api', csrf_exempt(views.increase_api_detail), name='increase-api-detail'),
    path('user-preference', csrf_exempt(views.user_preferences), name='user_preference'),
    path('detail-stock/<int:id>/user-preference', csrf_exempt(views.user_preferences_detail),
         name='user_preference_detail')
]

