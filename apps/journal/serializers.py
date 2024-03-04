from rest_framework import serializers

from .models import *
from .models import Emotion




class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['name']
class SubEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['name', 'description', 'image']
        
        
        
class FilterSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)


class MoodPrimaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodPrimaryEntry
        fields = ["mood", "date"]
        read_only_fields = ["date"]


class MoodSecondEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodSecondEntry
        fields = ["mood", "date"]
        read_only_fields = ["date"]

