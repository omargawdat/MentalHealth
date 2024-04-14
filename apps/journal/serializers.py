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
        

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ["notes", "date"]
        read_only_fields = ["date"]
        
class ActivityEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEntry
        fields = ["activity", "date"]
        read_only_fields = ["date"]

class ReasonEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonEntry
        fields = ["reason", "date"]
        read_only_fields = ["date"]
        
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'    
        
   
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PreferenceSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = Preference
        fields = ('id', 'question_text', 'tag', 'option1', 'option2')