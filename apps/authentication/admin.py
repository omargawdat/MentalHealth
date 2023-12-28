# register models
# Path: apps/authentication/admin.py

from django.contrib import admin

from .models import CustomUser

admin.site.register(CustomUser)
