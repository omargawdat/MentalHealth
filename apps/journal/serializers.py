from rest_framework import serializers

from .models import Journal


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["content", "date", "title"]
        read_only_fields = ["date"]
