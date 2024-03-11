from django.db import models

from apps.authentication.models import CustomUser


class Emotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='emotions/', blank=True, null=True)
    type = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "emotions"


class MoodPrimaryEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mood = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')


class MoodSecondEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mood = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
