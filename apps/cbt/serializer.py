from rest_framework import serializers

from .models import NegativeThinkingType, CBTQuestion


class NegativeThinkingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeThinkingType
        fields = ['id', 'name', 'explanation', 'tips']


class CBTQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CBTQuestion
        fields = ['id', 'question_text', 'thinking_type', 'is_general', 'after_question_tip']
