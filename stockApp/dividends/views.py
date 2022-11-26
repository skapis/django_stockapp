import datetime
from django.shortcuts import render, redirect
from stocks.models import Stock
from transactions.models import Transaction
from users.models import UserProfile, Currency
from .models import Dividend
from django.core.paginator import Paginator
import decimal
import requests as r
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
import csv
import xlwt


@login_required(login_url='/authentication/login')
def index(request):
    stocks = Stock.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(owner=request.user)
    dividends = Dividend.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)
    # paginator = Paginator(dividends, 5)
    # page_number = request.GET.get('page')
    # page_obj = Paginator.get_page(paginator, page_number)
    total_dividends = 0
    cur_value = 0
    total_value = 0
    if profile.currency == 'USD':
        rate = 1
    else:
        rate = decimal.Decimal(r.get('https://api.exchangerate.host/latest?base=USD').json()['rates'][profile.currency])
    for stock in stocks:
        shares = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
        if len(shares) != 0:
            share_amount = shares.aggregate(shares_count=Sum('shares'))
            total_dividends += (decimal.Decimal(stock.lastDiv) * share_amount['shares_count'] * rate)
            cur_value += (decimal.Decimal(stock.price) * share_amount['shares_count'] * rate)

    for transaction in transactions:
        total_value += (transaction.cost_share * transaction.shares)

    total = round(total_dividends, 2)
    if total_value or cur_value != 0:
        div_market = round((total/cur_value) * 100, 2)
        div_investment = round((total/total_value) * 100, 2)
    else:
        div_market = 0
        div_investment = 0

    total_acq = dividends.aggregate(div=Sum('amount'))

    context = {
        'total_dividends': total,
        'dividend_investment': div_investment,
        'div_market': div_market,
        'dividends': dividends,
        'acquired_div': total_acq['div'],
        'currency': currency,
        # 'page_obj': page_obj
    }
    return render(request, 'dividends/index.html', context)


def div_by_stock(request):
    stocks = Stock.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    stock_div = 0
    response = {}

    for stock in stocks:
        shares = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
        if len(shares) != 0:
            share_amount = shares.aggregate(shares_count=Sum('shares'))
            stock_div += (decimal.Decimal(stock.lastDiv) * share_amount['shares_count'])
            response.update({stock.symbol: stock_div})
            stock_div = 0

    return JsonResponse(response)


@login_required(login_url='/authentication/login')
def add_dividend(request):
    stocks = Stock.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    context = {
        'stock': stocks,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'dividends/add_dividend.html', {'stocks': stocks, 'context': context})

    if request.method == 'POST':

        symbol = request.POST['symbol']
        amount = request.POST['amount']
        date = request.POST['div_date']

        stock = Stock.objects.get(owner=request.user, symbol=symbol)

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'dividends/add_dividend.html', {'stocks': stocks, 'context': context})

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'dividends/add_dividend.html', {'stocks': stocks, 'context': context})

        Dividend.objects.create(symbol=symbol, amount=amount, date=date, stock_id=stock, owner=request.user)

        messages.success(request, 'Record was succesfully saved')
        return redirect('dividend_dashboard')


@login_required(login_url='/authentication/login')
def edit_dividend(request, id):
    try:
        dividend = Dividend.objects.get(pk=id)
    except:
        messages.error(request, 'Required dividend record does not exist')
        return render(request, '404_page.html')

    if request.user != dividend.owner:
        messages.error(request, 'You do not have access to see this page')
        return render(request, '404_page.html')

    stocks = Stock.objects.filter(owner=request.user)
    context = {
        'dividend': dividend
    }
    if request.method == 'GET':
        return render(request, 'dividends/edit_dividend.html', {'stocks': stocks, 'context': context})

    if request.method == 'POST':
        stock = request.POST['symbol']

        if not request.POST['amount']:
            messages.error(request, 'Amount is required')
            return render(request, 'dividends/edit_dividend.html', {'stocks': stocks, 'context': context})

        amount = request.POST['amount']
        date = request.POST['div_date']

        dividend.symbol = stock
        dividend.amount = amount
        dividend.date = date
        dividend.save()

        messages.success(request, 'Record was succesfully edited')
        return redirect('dividend_dashboard')


@login_required(login_url='/authentication/login')
def detail_dividend(request, id):
    try:
        dividend = Dividend.objects.get(pk=id)
    except:
        messages.error(request, 'Required dividend record does not exist')
        return render(request, '404_page.html')

    if request.user != dividend.owner:
        messages.error(request, 'You do not have access to see this page')
        return render(request, '404_page.html')

    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)

    context = {
        'dividend': dividend,
        'currency': currency,
    }

    return render(request, 'dividends/detail_dividend.html', context)


def delete_dividend(request, id):
    dividend = Dividend.objects.get(pk=id)
    dividend.delete()
    messages.success(request, 'Record was succesfully removed')
    return redirect('dividend_dashboard')


def dividend_by_year(request):
    dividends = Dividend.objects.filter(owner=request.user).values_list('symbol', 'date', 'amount')
    profile = UserProfile.objects.get(owner=request.user)

    symbols = []
    date = []
    amount = []
    for dividend in dividends:
        symbols.append(dividend[0])
        year = datetime.datetime.strptime(str(dividend[1]), '%Y-%m-%d')
        date.append(year.year)
        amount.append(dividend[2])
    d = {'symbol': symbols, 'year': date, 'amount': amount}
    df = pd.DataFrame(data=d)
    data = df.groupby('year')['amount'].sum().to_dict()
    return JsonResponse(data)


def export_div_csv(request):
    profile = UserProfile.objects.get(owner=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Dividends_' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Symbol', 'Amount', 'Date'])
    dividends = Dividend.objects.filter(owner=request.user)

    for dividend in dividends:
        writer.writerow([dividend.symbol, dividend.amount, dividend.date])

    return response


def export_div_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Dividends_' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Dividends')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Symbol', 'Amount', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Dividend.objects.filter(owner=request.user)\
        .values_list('symbol', 'amount', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


