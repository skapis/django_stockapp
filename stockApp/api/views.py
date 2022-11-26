from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserAPI
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from transactions.models import Transaction
from dividends.models import Dividend
from django.db.models import Q
from datetime import datetime


@login_required(login_url='/authentication/login')
def generate_key(request):
    if request.method == 'GET':
        user = request.user
        api_key = str(uuid.uuid4())

        user_api = UserAPI.objects.get(owner=request.user)
        if user_api.is_active:
            user_api.api_key = api_key
            user_api.save()
            messages.success(request, 'Your API key was changed')
            return redirect('account')

        user_api.api_key = api_key
        user_api.is_active = True
        user_api.save()
        messages.success(request, 'Your API was activated')
        return redirect('account')


@login_required(login_url='/authentication/login')
def deactivate_api(request):
    if request.method == 'GET':
        user_api = UserAPI.objects.get(owner=request.user)
        user_api.api_key = None
        user_api.is_active = False
        user_api.save()

        messages.success(request, 'Your API was deactivated')
        return redirect('account')


def documentation(request):
    user_api = UserAPI.objects.get(owner=request.user)
    context = {
        'user_api': user_api
    }
    return render(request, 'api/documentation.html', context)


def transactions_api(request, api_key):
    try:
        user = UserAPI.objects.get(api_key=api_key)
        symbol = request.GET.get('symbol')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if symbol is None:
            symbol = ''
        if date_from is None:
            date_from = '1900-01-01'
        if date_to is None:
            date_to = datetime.now().date()
        transactions = Transaction.objects.filter(Q(owner=user.owner) &
                                                  Q(symbol__startswith=symbol) &
                                                  Q(date__gte=date_from) &
                                                  Q(date__lte=date_to))
        total = transactions.count()
        if request.method == 'GET':
            response = {
                'total': total
            }
            items = []
            for transaction in transactions:
                tr = {
                    'symbol': transaction.symbol,
                    'date': transaction.date,
                    'cost_share': transaction.cost_share,
                    'broker': transaction.broker,
                    'shares': transaction.shares,
                    'fee': transaction.fee_amount
                }
                items.append(tr)
            response.update({'items': items})
            return JsonResponse(response, status=200)
    except:
       return JsonResponse({'info': 'API key is wrong'}, status=401)


def dividend_api(request, api_key):
    try:
        user = UserAPI.objects.get(api_key=api_key)
        symbol = request.GET.get('symbol')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if symbol is None:
            symbol = ''
        if date_from is None:
            date_from = '1900-01-01'
        if date_to is None:
            date_to = datetime.now().date()
        dividends = Dividend.objects.filter(Q(owner=user.owner) &
                                            Q(symbol__startswith=symbol) &
                                            Q(date__gte=date_from) &
                                            Q(date__lte=date_to))
        total = dividends.count()
        if request.method == 'GET':
            response = {
                'total': total
            }
            items = []
            for dividend in dividends:
                tr = {
                    'symbol': dividend.symbol,
                    'date': dividend.date,
                    'amount': dividend.amount,
                }
                items.append(tr)
            response.update({'items': items})
            return JsonResponse(response, status=200)
    except:
       return JsonResponse({'info': 'API key is wrong'}, status=401)

