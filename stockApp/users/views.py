from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Premium, Currency
from django.http import JsonResponse
from stocks.models import Stock
from api.models import UserAPI
import json
import os


@login_required(login_url='/authentication/login')
def index(request):
    stocks = Stock.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    profile.companies = stocks.count()
    profile.save()
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(owner=request.user)
    premium = Premium.objects.get(pk=profile.premium_plan)
    user_api = UserAPI.objects.get(owner=request.user)
    context = {
        'user': user,
        'profile': profile,
        'premium': premium,
        'api': user_api
    }
    return render(request, 'users/index.html', context)


@login_required(login_url='/authentication/login')
def edit_user(request):
    user = User.objects.get(username=request.user)
    context = {
        'user': user
    }

    if request.method == 'GET':
        return render(request, 'users/edit_user.html', context)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'The user data was succesfully changed')
        return redirect('account')


@login_required(login_url='/authentication/login')
def change_password(request):
    user = User.objects.get(username=request.user)
    context = {
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'users/change_password.html')

    if request.method == 'POST':
        oldpsw = request.POST['oldpsw']
        newpsw = request.POST['psw']
        psw_conf = request.POST['pswc']

        if not user.check_password(oldpsw):
            messages.error(request, "Old password is wrong, please try again")
            return render(request, 'users/change_password.html')

        if oldpsw == newpsw:
            messages.error(request, "New password cannot be old password, please try again")
            return render(request, 'users/change_password.html', context)

        if len(newpsw) < 6:
            messages.error(request, 'Password is too short')
            return render(request, 'users/change_password.html', context)

        if newpsw != psw_conf:
            messages.error(request, "Passwords are different, please try again")
            return render(request, 'users/change_password.html', context)

        user.set_password(newpsw)
        user.save()
        messages.success(request, 'Password was changed, please sign in again')
        return redirect('account')


def create_profile(request):
    user = request.user
    currency = 'USD'
    premium = True
    premium_plan = 'Unlimited'
    company_limit = 250
    api_limit = 250

    UserProfile.objects.create()

    return redirect('dashboard')


def change_currency(request):
    user = request.user
    profile = UserProfile.objects.get(owner=user)
    currency = Currency.objects.all()

    context = {
        'currencies': currency
    }

    if request.method == 'GET':
        return render(request, 'users/change_currency.html', context)

    if request.method == 'POST':
        new_currency = request.POST['currency']

        profile.currency = new_currency
        profile.save()

        messages.success(request, 'Currency was succesfully changed')
        return redirect('account')

