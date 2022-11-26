from django.shortcuts import render, redirect
from users.models import UserProfile, Premium
from product.models import Catalog, Users_prod
from django.contrib import messages
from django.views import View
import uuid
from datetime import datetime, timedelta
import threading
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def index(request):
    profile = UserProfile.objects.get(owner=request.user)
    premium = Premium.objects.get(pk=profile.premium_plan)
    context = {
        'premium': premium
    }
    if request.method == 'GET':
        return render(request, 'premium/index.html', context)


def confirm(request, id):
    user = request.user
    profile = UserProfile.objects.get(owner=user)
    premium = Premium.objects.get(pk=profile.premium_plan)
    requested = Premium.objects.get(pk=id)
    context = {
        'user': user,
        'profile': profile,
        'cur_premium': premium,
        'requested': requested
    }
    if request.method == 'GET':
        return render(request, 'premium/confirm.html', context)
    if request.method == 'POST':
        order_id = str(uuid.uuid4())
        Users_prod.objects.create(owner=request.user, product_id=requested.pk, product_name=requested.plan,
                                  active_from='1900-01-01', active_to='1900-01-01', order_id=order_id,
                                  order_date=datetime.now().date())
        messages.success(request, 'Your order was confirmed, please follow instruction in email')
        current_site = get_current_site(request)
        product = Users_prod.objects.get(order_id=order_id)
        email_contents = {
            'product': product,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(product.pk)),
            'token': token_generator.make_token(product)
        }
        link = reverse('product_activation', kwargs={
            'uidb64': email_contents['uid'], 'token': email_contents['token']})

        email_subject = f'Payment instructions for order {order_id}'
        activate_url = f"http://{current_site.domain}{link}"

        email = EmailMessage(
            email_subject,
            f'Hi there, Please click the link below to activate your product {activate_url}',
            'noreply@expenses.com',
            [user.email]
        )
        EmailThread(email).start()
        return redirect('payment', order_id)


def payment_instructions(request, order_id):
    product = Users_prod.objects.get(order_id=order_id)
    premium = Premium.objects.get(plan=product.product_name)
    context = {
        'user': request.user,
        'product': product,
        'premium': premium
    }
    return render(request, 'premium/payment.html', context)


class Product_activation(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        product = Users_prod.objects.get(pk=id)
        profile = UserProfile.objects.get(owner_id=product.owner_id)
        premium = Premium.objects.get(plan=product.product_name)
        if not token_generator.check_token(product, token):
            messages.warning(request, 'Product is already activated')
            return redirect('dashboard')

        if product.is_active:
            return redirect('dashboard')
        product.active_from = datetime.now().date()
        product.active_to = datetime.now().date() + timedelta(days=30)
        product.payment = True
        product.is_active = True
        product.save()
        profile.premium_plan = premium.pk
        profile.save()

        messages.success(request, 'Product is activated')
        return redirect('dashboard')



