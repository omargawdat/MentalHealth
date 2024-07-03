# apps/plan/serializers.py
from rest_framework import serializers
from .models import DepActivity, Topic, Activity,UserActivity
from apps.journal.serializers import TagSerializer

class TopicSerializer(serializers.ModelSerializer):
    enrolled = serializers.SerializerMethodField()
    class Meta:
        model = Topic
        fields = ('id', 'name', 'color', 'image', 'description', 'enrolled')
    def get_enrolled(self, obj):
        user = self.context['request'].user
        return UserActivity.objects.filter(user=user, topic=obj).exists()
    
class ActivitySerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = Activity
        fields = ('text', 'tag')


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ('number', 'flag', 'text')


class TopicWithActivitiesSerializer(serializers.ModelSerializer):
    activities = UserActivitySerializer(many=True, source='useractivity_set')

    class Meta:
        model = Topic
        fields = ('id', 'name', 'color', 'image', 'activities')


class DepActivitySerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    level = serializers.StringRelatedField()  
    class Meta:
        model = DepActivity
        fields = ('text', 'tag', 'level')

class ActivityNumberSerializer(serializers.Serializer):
    number = serializers.IntegerField()