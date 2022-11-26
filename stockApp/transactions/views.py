import os.path
from django.conf import settings
from django.shortcuts import render, redirect
import json
import requests as r
from .models import Broker, Transaction
from stocks.models import Stock
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
import datetime
import csv
import xlwt
from users.models import UserProfile, Premium, Currency
import decimal


@login_required(login_url='/authentication/login')
def index(request):
    transactions = Transaction.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)

    context = {
        'transactions': transactions,
        'currency': currency,
    }
    return render(request, 'transactions/index.html', context)


@login_required(login_url='/authentication/login')
def add_transaction_user(request):
    user_stocks = Stock.objects.filter(owner=request.user)
    brokers = Broker.objects.all()
    profile = UserProfile.objects.get(owner=request.user)
    premium = Premium.objects.get(pk=profile.premium_plan)
    limit = premium.api_limit
    user_api = profile.api_requests

    if limit <= user_api:
        api_limit = 'exceed'
    else:
        api_limit = 'available'

    context = {
        'user_stocks': user_stocks,
        'brokers': brokers,
        'values': request.POST,
        'api': api_limit
    }
    if request.method == 'GET':
        return render(request, 'transactions/add_transaction.html', context)

    if request.method == 'POST':
        symbol = request.POST['symbol']

        share_price = request.POST['share_price']
        fee_amount = request.POST['fee_amount']

        if not share_price:
            messages.error(request, 'Share price is required')
            return render(request, 'transactions/add_transaction.html', context)

        broker = request.POST['broker']
        date = request.POST['transaction_date']
        tr_type = 'Buy'
        shares = request.POST['amount']

        if fee_amount != 0:
            fee = True
        else:
            fee = False

        cur_stock = Stock.objects.get(owner=request.user, symbol=symbol)

        if not shares:
            messages.error(request, 'Amount is required')
            return render(request, 'transactions/add_transaction.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'transactions/add_transaction.html', context)

        Transaction.objects.create(owner=request.user, symbol=symbol, shares=shares, cost_share=share_price,
                                   date=date, broker=broker, tr_type=tr_type, stock_id=cur_stock,
                                   stock_price=cur_stock.price, fee=fee, fee_amount=fee_amount)
        messages.success(request, "Transaction was succesfully saved")
        return redirect('transactions')


@login_required(login_url='/authentication/login')
def edit_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
    except:
        messages.error(request, 'Required transaction does not exist')
        return render(request, '404_page.html')

    if request.user != transaction.owner:
        messages.error(request, 'You do not have access to see this page')
        return render(request, '404_page.html')

    broker = Broker.objects.all()
    user_stocks = Stock.objects.filter(owner=request.user)

    context = {
        'transaction': transaction,
        'brokers': broker,
        'user_stocks': user_stocks
    }
    if request.method == 'GET':
        return render(request, 'transactions/edit_transaction.html', context)

    if request.method == 'POST':

        symbol = request.POST['symbol']
        share_price = request.POST['share_price']

        if not share_price:
            messages.error(request, 'Share price is required')
            return render(request, 'transactions/edit_transaction.html', context)

        broker = request.POST['broker']
        date = request.POST['transaction_date']
        shares = request.POST['amount']
        fee = request.POST['fee_amount']

        if not shares:
            messages.error(request, 'Amount is required')
            return render(request, 'transactions/edit_transaction.html', context)

        transaction.owner = request.user
        transaction.symbol = symbol
        transaction.cost_share = share_price
        transaction.shares = shares
        transaction.broker = broker
        transaction.fee_amount = fee
        transaction.date = date

        transaction.save()

        messages.success(request, "Transaction was succesfully changed")

        return redirect('transactions')  # TODO: return user to stock detail, if he edit transaction from detail


@login_required(login_url='/authentication/login')
def detail_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
    except:
        messages.error(request, 'Required transaction does not exist')
        return render(request, '404_page.html')

    if request.user != transaction.owner:
        messages.error(request, 'You do not have access to see this page')
        return render(request, '404_page.html')

    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)

    context = {
        'transaction': transaction,
        'currency': currency,
    }
    return render(request, 'transactions/detail_transaction.html', context)


@login_required(login_url='/authentication/login')
def delete_transaction(request, id):
    transaction = Transaction.objects.get(pk=id)
    stock = Stock.objects.get(owner=request.user, symbol=transaction.symbol)
    transaction.delete()
    messages.success(request, 'Transaction was succesfully removed')
    if 'detail-stock' in request.META['HTTP_REFERER']:
        return redirect('detail_stock', stock.id)
    else:
        return redirect('transactions')


@login_required(login_url='/authentication/login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Transactions_' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Symbol', 'Share Price', 'Fee', 'Amount', 'Broker', 'Type', 'Date'])
    transactions = Transaction.objects.filter(owner=request.user)

    for transaction in transactions:
        writer.writerow([transaction.symbol, transaction.cost_share, transaction.shares, transaction.fee_amount,
                         transaction.broker, transaction.tr_type, transaction.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Transactions_' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transactions')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Symbol', 'Share Price', 'Amount', 'Fee', 'Broker', 'Type', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Transaction.objects.filter(owner=request.user)\
        .values_list('symbol', 'cost_share', 'shares', 'fee_amount', 'broker', 'tr_type', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


@login_required(login_url='/authentication/login')
def check_api(request):
    if request.method == 'GET':
        profile = UserProfile.objects.get(owner=request.user)
        premium = Premium.objects.get(pk=profile.premium_plan)
        return JsonResponse({'remainingRequests': premium.api_limit - profile.api_requests})


@login_required(login_url='/authentication/login')
def increase_api(request):
    if request.method == 'GET':
        profile = UserProfile.objects.get(owner=request.user)
        premium = Premium.objects.get(pk=profile.premium_plan)
        if premium.api_limit != profile.api_requests:
            profile.api_requests += 1
            profile.save()
        return JsonResponse({'remainingRequests': premium.api_limit - profile.api_requests})


@login_required(login_url='/authentication/login')
def user_preferences(request):
    profile = UserProfile.objects.get(owner=request.user)
    return JsonResponse({'preferences': profile.currency})
