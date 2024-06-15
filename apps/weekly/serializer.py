from rest_framework import serializers

from .models import LifeAspectType, LifeAspect


class LifeAspectSerializer(serializers.ModelSerializer):
    aspect_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LifeAspectType.objects.all(), source='aspect_type', write_only=True
    )
    aspect_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LifeAspect
        fields = ['id', 'aspect_type_id', 'aspect_type', 'value', 'date']


class LifeAspectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeAspectType
        fields = ['id', 'name']
