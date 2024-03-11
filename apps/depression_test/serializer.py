from rest_framework import serializers
from .models import DepressionTestAttempt


class DepressionTestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepressionTestAttempt
        fields = ['total_score', 'level_of_depression', 'timestamp']
