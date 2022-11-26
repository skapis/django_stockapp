from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def home(request):
    return render(request, 'startpage/home.html')


def plans(request):
    return render(request, 'startpage/plans.html')


def about(request):
    return render(request, 'startpage/about.html')


def contact(request):
    if request.method == 'GET':
        return render(request, 'startpage/contact.html')

    if request.method == 'POST':
        email_address = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        context = {
            'values': request.POST
        }
        if not email_address:
            messages.error(request, 'Email is required')
            return render(request, 'startpage/contact.html', context)
        if not subject:
            messages.error(request, 'Subject is required')
            return render(request, 'startpage/contact.html', context)
        if not message:
            messages.error(request, 'Message is required')
            return render(request, 'startpage/contact.html', context)

        email_subject = f"Contact form PortfolioApp - {subject}"

        email = EmailMessage(
            email_subject,
            f'Sender: {email_address}\n{message}',
            'noreply@expenses.com',
            ['jakub.skapik@gmail.com']
        )
        EmailThread(email).start()
        messages.success(request, 'Thank you for your feedback')
        return redirect('contact')


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        return JsonResponse({'email_valid': True})
