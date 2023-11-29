from django.db import models
from django.utils import timezone

from apps.authentication.models import CustomUser


class Journal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)


class Emotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='emotions/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_emotions',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "emotions"


class EmotionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'date')
