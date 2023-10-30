from rest_framework import serializers

from .models import AnswerOption, TestQuestion


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ['question']


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['value', 'label']


def validate_number_of_answers(value):
    number_of_questions = TestQuestion.objects.count()
    if len(value) != number_of_questions:
        raise serializers.ValidationError(
            f"The number of answers provided ({len(value)}) does not match the number of questions ({number_of_questions})."
        )
    return value


def validate_numbers(value):
    for num in value:
        if not isinstance(num, int) or num < 0 or num > 4:
            raise serializers.ValidationError(
                "All numbers must be integers between 0 and 4."
            )
    return value


class SumNumbersSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(),
        validators=[validate_numbers, validate_number_of_answers],
        min_length=1
    )
