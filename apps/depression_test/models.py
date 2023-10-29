from django.db import models


from django.db import models

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
