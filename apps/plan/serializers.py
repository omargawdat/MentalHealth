# apps/plan/serializers.py
from rest_framework import serializers
from .models import Topic, Activity,UserActivity
from apps.journal.serializers import TagSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'color', 'image')

class ActivitySerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = Activity
        fields = ('text', 'tag')


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ('number', 'flag')
        
class TopicWithActivitiesSerializer(serializers.ModelSerializer):
    activities = UserActivitySerializer(many=True, source='useractivity_set')

    class Meta:
        model = Topic
        fields = ('id', 'name', 'color', 'image', 'activities')
