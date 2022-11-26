from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dividend_dashboard'),
    path('by_stock', views.div_by_stock, name='div_by_stock'),
    path('add-record', views.add_dividend, name='add_dividend'),
    path('delete-div/<int:id>', views.delete_dividend, name='delete_dividend'),
    path('detail/<int:id>', views.detail_dividend, name='detail_dividend'),
    path('edit/<int:id>', views.edit_dividend, name='edit_dividend'),
    path('dividend_by_year', views.dividend_by_year, name='dividend_by_year'),
    path('export-dividends-csv', views.export_div_csv, name='export_div_csv'),
    path('export-dividends-xls', views.export_div_excel, name='export_div_excel')
]