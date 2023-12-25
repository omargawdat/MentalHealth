import random

from django.conf import settings
from django.core.mail import send_mail


def send_otp_via_email(email, action):
    subject = 'Your Account Verification email'
    otp = random.randint(1000, 9999)
    message = f'Your otp for verification code for the best mental health app for {action}: {otp}'
    try:
        send_mail(subject, message, settings.EMAIL_HOST, [email])
    except Exception as e:
        print(e)
    return otp
