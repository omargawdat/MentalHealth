# models.py
from django.db import models


class Emotion(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='emotions/')

    def __str__(self):
        return self.name


class SubEmotion(models.Model):
    emotion = models.ForeignKey(Emotion, related_name='sub_emotions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sub_emotions/')
    tip = models.TextField()
    explanation = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.emotion.name})"


class Activity(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='activities/')

    def __str__(self):
        return self.name


class Reason(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='reasons/')

    def __str__(self):
        return self.name
