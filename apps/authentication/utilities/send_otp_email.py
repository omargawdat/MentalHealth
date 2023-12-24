# from django.conf import settings
# from django.core.mail import BadHeaderError, send_mail
#
#
# def send_otp_email(user, otp):
#     try:
#
#         subject = 'Your OTP for Account Verification'
#         # message = f'Your OTP is: {otp}'
#
#         message = f'Hello,\n\nYour OTP is: {otp}\n\nPlease use this code to complete your account verification.\n\nWelcome to our website!'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [user.email]
#         send_mail(subject, message, email_from, recipient_list)
#     except BadHeaderError:
#         print("wtf1")
#         pass
import random

from django.conf import settings
from django.core.mail import send_mail


def send_otp_via_email(email):
    subject = 'Your Account Verification email'
    otp = random.randint(1000, 9999)
    message = f'Your otp for verification code for the best mental health app: {otp}'
    try:
        send_mail(subject, message, settings.EMAIL_HOST, [email])
    except Exception as e:
        print(e)
    return otp
