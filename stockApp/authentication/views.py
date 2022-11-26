from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from users.models import UserProfile, Currency
from api.models import UserAPI


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'This User is already exists'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already taken'}, status=409)
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # plan = request.POST['plan'] TODO: in future user can select plan during creating account

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # if plan == 'Free':
                #     premium_id = 1
                #     premium_set = False
                # elif plan == 'Trader':
                #     premium_id = 2
                #     premium_set = True
                # else:
                #     premium_id = 3
                #     premium_set = True
                # TODO: replace with enumeration of plans/products

                UserProfile.objects.create(currency='USD', premium=False, premium_plan=1,
                                           owner=user, api_requests=0, companies=0, api_renewal=datetime.now().date())

                UserAPI.objects.create(owner=user)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = f"http://{domain}{link}"
            email_subject = 'Activate your account'
            email_body = f"Hi {user.username},\nPlease use this link to verify your account\n{activate_url}"
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@expenses.com',
                [email]
            )
            email.send(fail_silently=False)
            messages.success(request,
                             'Account was succesfully created, please check your email to activate your account')
            return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        #try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        currency = Currency.objects.all()
        if not token_generator.check_token(user, token):
            return redirect('login'+'?message='+'User already activated')

        if user.is_active:
            messages.info(request, 'Account is already activated, please login')
            return redirect('login')
        user.is_active = True
        user.save()

        context = {
            'currencies': currency,
            'token': token,
            'uidb64': uidb64
        }
        messages.success(request, 'Account is activated, please complete your registration')
        return render(request, 'authentication/complete_registration.html', context)

        #except Exception as ex:
         #   pass

    def post(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        profile = UserProfile.objects.get(owner=user)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        currency = request.POST['currency']

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile.currency = currency
        profile.save()

        messages.success(request, 'Your registration is complete, please login')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    profile = UserProfile.objects.get(owner=user)
                    if profile.api_renewal != datetime.now().date():
                        profile.api_renewal = datetime.now().date()
                        profile.api_requests = 0
                        profile.save()
                    messages.success(request, f'Welcome {user.username} you are now logged in')
                    return redirect('dashboard')
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Username or password is wrong, please check your credentials')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields')

        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been sucessfully logout')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/psw_reset.html')

    def post(self, request):
        email = request.POST['email']
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'authentication/psw_reset.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }
            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password reset Instructions'
            reset_url = f"http://{current_site.domain}{link}"

            email = EmailMessage(
                email_subject,
                f'Hi there, Please click the link below to reset your password {reset_url}',
                'noreply@expenses.com',
                [email]
            )
            EmailThread(email).start()
            messages.success(request, 'We have sent you an email to reset your password')

        return render(request, 'authentication/psw_reset.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }

        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password is too short')
            return render(request, 'authentication/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password link is invalid, please request a new one")
                return render(request, 'authentication/set-new-password.html', context)

            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succesfully')

            return redirect('login')

        except Exception as identifier:
            messages.info(request, 'Something went wrong')
            return render(request, 'authentication/set-new-password.html', context)
