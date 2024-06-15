from django.db import models


class NegativeThinkingType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    explanation = models.TextField()
    tips = models.TextField()

    def __str__(self):
        return self.name


class CBTQuestion(models.Model):
    question_text = models.TextField()
    thinking_type = models.ForeignKey(NegativeThinkingType, on_delete=models.CASCADE, related_name='questions',
                                      null=True, blank=True)
    is_general = models.BooleanField(default=False)
    after_question_tip = models.TextField(blank=True)

    def __str__(self):
        return self.question_text
