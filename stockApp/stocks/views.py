from django.shortcuts import render, redirect
from .models import Stock
from django.conf import settings
import os
from transactions.models import Transaction, Broker
from users.models import UserProfile, Premium, Currency
from dividends.models import Dividend
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import uuid
from django.db.models import Sum
import requests as r
from datetime import datetime
import decimal
from django.http import JsonResponse
import pandas as pd
from django.utils.safestring import mark_safe


@login_required(login_url='/authentication/login')
def index(request):
    stocks = Stock.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)
    premium = Premium.objects.get(pk=profile.premium_plan)
    total_amount = stocks.count()
    total_value = 0
    cur_value = 0
    api = 0
    total_cost = 0

    if profile.currency == 'USD':
        rate = 1
    else:
        rate = decimal.Decimal(r.get('https://api.exchangerate.host/latest?base=USD').json()['rates'][profile.currency])

    if premium.company_limit == profile.companies:
        company_limit = 'exceed'
    else:
        company_limit = 'available'

    if (premium.api_limit - profile.api_requests) < len(stocks):
        as_of = stocks[0].price_date
        messages.error(request, f"Your API limit is too low to refresh your data. Data are as of {as_of}.")
        messages.info(request, mark_safe("If you need more requests or companies, you can upgrade your premium plan\
                        <a href='/premium/upgrade'>here</a>"))

        for stock in stocks:
            cur_price = stock.price
            shares = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
            if len(shares) != 0:
                share_amount = shares.aggregate(shares_count=Sum('shares'))
                for tr in shares:
                    total_cost += ((tr.cost_share * tr.shares) + tr.fee_amount)
                stock.total_value = round(total_cost, 2)
                stock.avg_price = round(total_cost/share_amount['shares_count'], 2)
                stock.total_amount = share_amount['shares_count']
                stock.cur_value = round((decimal.Decimal(stock.price) * share_amount['shares_count']), 2)
                stock.save()
                cur_value += (decimal.Decimal(stock.price) * share_amount['shares_count'] * rate)
                total_cost = 0
    else:
        # refresh current prices of user stocks
        for stock in stocks:
            if stock.price_date != datetime.now().date():
                url = f"https://financialmodelingprep.com/api/v3/profile/{stock.symbol}?apikey="
                data = r.get(url).json()
                cur_price = data[0]['price']
                stock.price = cur_price
                stock.price_date = datetime.now().date()
                stock.lastDiv = data[0]['lastDiv']
                stock.save()
                api += 1
            shares = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
            if len(shares) != 0:
                share_amount = shares.aggregate(shares_count=Sum('shares'))
                for tr in shares:
                    total_cost += (tr.cost_share * tr.shares) + tr.fee_amount
                stock.total_value = round(total_cost, 2)
                stock.avg_price = round(total_cost/share_amount['shares_count'], 2)
                stock.total_amount = share_amount['shares_count']
                stock.cur_value = round((decimal.Decimal(stock.price) * share_amount['shares_count'] * rate), 2)
                stock.save()
                cur_value += (decimal.Decimal(stock.price) * share_amount['shares_count'] * rate)
                total_cost = 0

        profile.api_requests = profile.api_requests + api
        profile.companies = len(stocks)
        profile.save()

    for transaction in transactions:
        total_value += ((transaction.cost_share * transaction.shares) + transaction.fee_amount)

    if total_value != 0:
        gain_loss_prc = round((cur_value-total_value)/total_value, 2)
    else:
        gain_loss_prc = 0

    context = {
        'stocks': stocks,
        'total_amount': total_amount,
        'total_value': round(total_value, 2),
        'cur_value': round(cur_value, 2),
        'gain_loss': round((cur_value - total_value), 2),
        'gain_loss_prc': gain_loss_prc,
        'companies': company_limit,
        'currency': currency,
        'rate': rate
    }
    return render(request, 'stocks/index.html', context)


@login_required(login_url='/authentication/login')
def add_stock(request):
    stock_data = []
    file_path = os.path.join(settings.BASE_DIR, 'stocks.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            stock_data.append({'name': k, 'value': v})

    brokers = Broker.objects.all()
    profile = UserProfile.objects.get(owner=request.user)
    premium = Premium.objects.get(pk=profile.premium_plan)
    limit = premium.api_limit
    user_api = profile.api_requests

    if limit <= user_api:
        api_limit = 'exceed'
    else:
        api_limit = 'available'

    if premium.company_limit == profile.companies:
        company_limit = 'exceed'
    else:
        company_limit = 'available'

    context = {
        'brokers': brokers,
        'values': request.POST,
        'api': api_limit,
        'companies': company_limit
    }

    if request.method == 'GET':
        return render(request, 'stocks/add_stock.html', {'stocks': stock_data, 'context': context})

    if request.method == 'POST':

        stock = request.POST['symbol']
        share_price = request.POST['share_price']
        fee_amount = request.POST['fee_amount']
        uid = str(uuid.uuid4())

        url = f"https://financialmodelingprep.com/api/v3/profile/{stock}?apikey="
        data = r.get(url).json()
        name = data[0]['companyName']
        cur_price = data[0]['price']
        sector = data[0]['sector']
        image = data[0]['image']
        description = data[0]['description']
        website = data[0]['website']
        industry = data[0]['industry']
        currency = data[0]['currency']
        lastDiv = data[0]['lastDiv']
        exchange = data[0]['exchangeShortName']

        stocks = Stock.objects.filter(owner=request.user, symbol=stock)

        if stocks.exists():
            messages.error(request, 'This stock is already in portfolio, please choose another one')
            return render(request, 'stocks/add_stock.html', {'stocks': stock_data, 'context': context})

        if not share_price:
            messages.error(request, 'Share price is required')
            return render(request, 'stocks/add_stock.html', {'stocks': stock_data, 'context': context})

        broker = request.POST['broker']
        date = request.POST['transaction_date']
        tr_type = 'Buy'
        shares = request.POST['amount']

        if fee_amount != 0:
            fee = True
        else:
            fee = False

        if not shares:
            messages.error(request, 'Amount is required')
            return render(request, 'stocks/add_stock.html', {'stocks': stock_data, 'context': context})

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'stocks/add_stock.html', {'stocks': stock_data, 'context': context})

        Stock.objects.create(owner=request.user, symbol=stock, name=name,
                             uid=uid, price=round(cur_price, 2), price_date=datetime.now().date(),
                             logo=image, sector=sector, company_desc=description, website=website,
                             industry=industry, currency=currency, lastDiv=lastDiv, exchange=exchange)

        cur_stock = Stock.objects.get(uid=uid)

        # add new transaction
        Transaction.objects.create(owner=request.user, symbol=stock, shares=shares, cost_share=share_price,
                                   date=date, broker=broker, tr_type=tr_type, stock_id=cur_stock,
                                   stock_price=cur_price, fee=fee, fee_amount=fee_amount)

        messages.success(request, 'Stock was succesfully added')
        return redirect('dashboard')


@login_required(login_url='/authentication/login')
def detail_stock(request, id):
    try:
        stock = Stock.objects.get(pk=id)
    except:
        messages.error(request, 'Required stock does not exist')
        return render(request, '404_page.html')

    if request.user != stock.owner:
        messages.error(request, 'You do not have access to see this page')
        return render(request, '404_page.html')

    transactions = Transaction.objects.filter(stock_id=id, owner=request.user)
    dividends = Dividend.objects.filter(owner=request.user, stock_id=id)
    profile = UserProfile.objects.get(owner=request.user)
    currency = Currency.objects.get(code=profile.currency)
    if profile.currency == 'USD':
        rate = 1
    else:
        rate = decimal.Decimal(r.get('https://api.exchangerate.host/latest?base=USD').json()['rates'][profile.currency])
    costs = 0
    cur_value = 0
    for transaction in transactions:
        costs += (transaction.cost_share * transaction.shares) + transaction.fee_amount
        cur_value += (decimal.Decimal(stock.price) * transaction.shares * rate)
    if len(transactions) != 0:
        shares_total = transactions.aggregate(shares_count=Sum('shares'))
        if shares_total['shares_count'] != 0:
            avg_price = round(costs/shares_total['shares_count'], 2)
        else:
            avg_price = 0
    else:
        avg_price = 0
        shares_total = {'shares_count': 0}

    context = {
        'stock': stock,
        'shares_count': shares_total,
        'costs': round(costs, 2),
        'avg_price': round(avg_price, 2),
        'cur_value': round(cur_value, 2),
        'currency': currency,
        'rate': rate
    }
    return render(request, 'stocks/detail_stock.html',
                  {'transactions': transactions, 'context': context, 'dividends': dividends})


@login_required(login_url='/authentication/login')
def add_transaction_from_detail(request, id):
    stock = Stock.objects.get(owner=request.user, pk=id)
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
        'stock': stock,
        'brokers': brokers,
        'values': request.POST,
        'api': api_limit
    }

    if request.method == 'GET':
        return render(request, 'stocks/add_transaction_from_detail.html', context)

    if request.method == 'POST':
        symbol = stock.symbol
        share_price = request.POST['share_price']
        fee_amount = request.POST['fee_amount']

        if not share_price:
            messages.error(request, 'Share price is required')
            return render(request, 'stocks/add_transaction_from_detail.html', context)

        broker = request.POST['broker']
        date = request.POST['transaction_date']
        tr_type = 'Buy'
        shares = request.POST['amount']

        if fee_amount != 0:
            fee = True
        else:
            fee = False

        if not shares:
            messages.error(request, 'Amount is required')
            return render(request, 'stocks/add_transaction_from_detail.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'stocks/add_transaction_from_detail.html', context)

        Transaction.objects.create(owner=request.user, symbol=symbol, shares=shares, cost_share=share_price,
                                   date=date, broker=broker, tr_type=tr_type, stock_id=stock, stock_price=stock.price,
                                   fee=fee, fee_amount=fee_amount)
        messages.success(request, "Transaction was succesfully saved")
        return redirect('detail_stock', stock.id)


def delete_stock(request, id):
    stock = Stock.objects.get(pk=id)
    stock.delete()
    messages.success(request, 'Stock was succesfully removed')
    return redirect('dashboard')


def value_by_stock(request):
    stocks = Stock.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    response = {}

    for stock in stocks:
        value = 0
        transactions = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
        shares = transactions.aggregate(shares_count=Sum('shares'))
        if not shares['shares_count'] is None:
            value += (shares['shares_count'] * stock.price)
            response.update({stock.symbol: round(value, 2)})
    return JsonResponse(response)


def value_by_sector(request):
    stocks = Stock.objects.filter(owner=request.user)
    response = {}
    symbols, values, sectors = [], [], []

    for stock in stocks:
        value = 0
        transactions = Transaction.objects.filter(owner=request.user, symbol=stock.symbol)
        shares = transactions.aggregate(shares_count=Sum('shares'))
        if not shares['shares_count'] is None:
            value += (shares['shares_count'] * stock.price)
            response.update({stock.symbol: value})
            symbols.append(stock.symbol)
            values.append(value)
            sectors.append(stock.sector)
    d = {'symbol': symbols, 'value': values, 'sector': sectors}
    df = pd.DataFrame(data=d)
    resp_list = df.groupby('sector')["value"].sum().to_dict()
    return JsonResponse(resp_list)


def portfolio_performance(request):
    transactions = Transaction.objects.filter(owner=request.user).order_by('date')
    profile = UserProfile.objects.get(owner=request.user)

    response = {}
    total_value = 0
    cur_value = 0
    for tr in transactions:
        total_value += (tr.cost_share * tr.shares) + tr.fee_amount
        cur_value += tr.shares * tr.stock_price
        response.update({str(tr.date): round(total_value, 2)})

    return JsonResponse(response)


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
def check_api_detail(request, id):
    if request.method == 'GET':
        profile = UserProfile.objects.get(owner=request.user)
        premium = Premium.objects.get(pk=profile.premium_plan)
        return JsonResponse({'remainingRequests': premium.api_limit - profile.api_requests})


@login_required(login_url='/authentication/login')
def increase_api_detail(request, id):
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


@login_required(login_url='/authentication/login')
def user_preferences_detail(request, id):
    profile = UserProfile.objects.get(owner=request.user)
    return JsonResponse({'preferences': profile.currency})







