from rest_framework import serializers

from .models import LifeAspect, LifeActivityTrack
from .models import LifeAspectType


class LifeAspectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeAspectType
        fields = ['id', 'name']


class LifeAspectSerializer(serializers.ModelSerializer):
    aspect_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LifeAspectType.objects.all(), source='aspect_type', write_only=True
    )
    aspect_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LifeAspect
        fields = ['id', 'aspect_type_id', 'aspect_type', 'value', 'date', ]

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is not None:
            validated_data['user'] = request.user
        return super().create(validated_data)


class LifeAspectHistorySerializer(serializers.ModelSerializer):
    aspect_type = serializers.StringRelatedField()

    class Meta:
        model = LifeAspect
        fields = ['aspect_type', 'value', 'date']


class LifeActivityTrackSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(source='life_activity.name', read_only=True)
    activity_description = serializers.CharField(source='life_activity.description', read_only=True)

    class Meta:
        model = LifeActivityTrack
        fields = ['id', 'activity_name', 'activity_description', 'created_at', 'is_checked']
