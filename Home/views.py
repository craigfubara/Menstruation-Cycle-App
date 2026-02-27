from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages


def index(request):
    return render(request, 'Home/home.html')


def faq(request):
    return render(request, 'Home/faq.html')


def pcod(request):
    return render(request, 'Home/pcod.html')


def selfcare(request):
    return render(request, 'Home/selfcare.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message_body = "\n".join(body.values())
            try:
                send_mail(subject, message_body, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Your message has been sent successfully!')
            return redirect("Home:home")
    else:
        form = ContactForm()
    return render(request, "Home/contact.html", {'form': form})
