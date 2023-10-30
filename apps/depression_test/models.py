from django.db import models

from apps.authentication.models import CustomUser
from apps.depression_test.constants import DepressionLevel


class AnswerOption(models.Model):
    value = models.IntegerField()
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TestQuestion(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class DepressionAssessment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assessments')
    total_score = models.PositiveIntegerField()
    level_of_depression = models.CharField(
        max_length=50,
        choices=[(level.value, level.value) for level in DepressionLevel]
    )
    date = models.DateField(auto_now_add=True)
