from rest_framework import serializers

from .models import *
from .models import Emotion


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["content", "date", "title"]
        read_only_fields = ["date"]


class EmotionSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name', 'description', 'image']


class EmotionSerializer(serializers.ModelSerializer):
    sub_emotions = EmotionSubSerializer(many=True, read_only=True)

    class Meta:
        model = Emotion
        fields = ['id', 'name', 'description', 'image', 'sub_emotions']


class EmotionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionHistory
        fields = ['id', 'emotion', 'date']
        read_only_fields = ['id']
