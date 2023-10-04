from rest_framework import serializers
from .models import jornalentry
from django.shortcuts import get_object_or_404
from .models import jornalentry
from apps.authentication.models import CustomUser

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = jornalentry
        fields = '__all__'