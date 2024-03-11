from django.db import models

from apps.authentication.models import CustomUser


class AnswerOption(models.Model):
    value = models.IntegerField()
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TestQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer_options = models.ManyToManyField(AnswerOption)

    def __str__(self):
        return self.question


class DepressionTestAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    level_of_depression = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp} - {self.level_of_depression}'
