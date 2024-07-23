from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from users.models import Contact

from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib import messages
from django.core.mail import EmailMessage

import os
from uuid import uuid4

from main.decorators import user_is_superuser
from .forms import NewsletterForm
from users.models import SubscribedUsers


# from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

# @login_required
def ourteam(request):
    return render(request, "our team.html")

def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(firstname=firstname,lastname=lastname, email=email, subject=subject, message=message, date= datetime.today())
        contact.save()
        
        send_mail(
            "Assistance with Login, Password Reset, Donations, and Book Purchases",
            f"Dear {firstname},\n"
        f"Thank you for reaching out to Helping Hand, and we sincerely appreciate your support and interest in our NGO's mission.\n"
        f"I understand that you are facing issues with various aspects of our platform, including login, password reset, donations, and purchasing books. Please know that we are here to assist you in resolving these issues promptly.\n\n"
        f"Login Issues:\nIf you are experiencing difficulty logging into your account, please follow these steps:\n\nEnsure that you are entering the correct email address and password.If you've forgotten your password, click on the Forgot Password link on the login page to reset it. You will receive instructions via email to create a new password.\n\n\n"
        f"Password Reset:\nIf you are having trouble resetting your password, please make sure to:\n\n"
        f"Check your spam or junk folder for the password reset email, as it might have been filtered there.\nAdd our email address (helping.hand.official.info@gmail.com) to your contact list to ensure you receive our emails.\nIf you are still facing issues, please let us know, and we will assist you further.\n\n\n"
        f"Donations:\nWe appreciate your generosity in supporting our cause. If you encounter any problems while making a donation, please:\n\n"
        f"Verify that your payment information is entered correctly.\nEnsure your payment method is accepted on our platform.\nIf you encounter any technical difficulties, kindly describe the issue in detail so that we can investigate and resolve it as soon as possible.\n\n\n"  
        f"Book Purchases:\nIf you are having issues purchasing books from our website, please:\n\n"
        f"Make sure you are following the correct steps for the purchase process.\nCheck if there are any error messages displayed during the purchase and provide us with those details.\nTo assist you more effectively, kindly provide us with the following information in your response:\n\n"   
        f"Your full name and email address associated with your account.\nA detailed description of the issue you are facing.\nAny error messages you have received.\nOur dedicated team will review your case promptly and work to resolve your issues. Rest assured, we are committed to ensuring that your experience with Helping Hand is smooth and enjoyable.\n\n\n"
        f"Thank you for your patience, understanding, and continued support. We apologize for any inconvenience you may have encountered and appreciate your commitment to our cause.\n"
        f"\n\nSincerely,\nHelping Hands\nhelping.hand.official.info@gmail.com",
            "helping.hand.offical.info@gmail.com",
            [email],
            fail_silently=False,
        )
    return render(request, "contact.html")


@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject')
            receivers = request.POST.get('receivers').split(',')
            email_message = request.POST.get('message')

            mail = EmailMessage(subject, email_message, f"Helping Hands <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent succesfully")
            else:
                messages.error(request, "There was an error sending email")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='newsletter.html', context={'form': form})