from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='transactions'),
    path('add-transaction', views.add_transaction_user, name='add_transaction'),
    path('edit-transaction/<int:id>', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:id>', views.delete_transaction, name='delete_transaction'),
    path('detail-transaction/<int:id>', views.detail_transaction, name='detail_transaction'),
    path('export-transactions-csv', views.export_csv, name='export_csv'),
    path('export-transactions-xls', views.export_excel, name='export_excel'),
    path('check-api', csrf_exempt(views.check_api), name='check-api'),
    path('increase-api', csrf_exempt(views.increase_api), name='increase-api'),
    path('user-preference', csrf_exempt(views.user_preferences), name='user_preference')
]