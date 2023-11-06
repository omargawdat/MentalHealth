from rest_framework import serializers
from .models import *


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["content", "date", "title"]
        read_only_fields = ["date"]

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['name']


        
class FilterSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    
    
class MoodPrimaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodPrimaryEntry
        fields = ["mood", "date"]
        read_only_fields = ["date"]
        
        
class MoodThirdEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodThirdEntry
        fields = ["mood", "date"]
        read_only_fields = ["date"]


