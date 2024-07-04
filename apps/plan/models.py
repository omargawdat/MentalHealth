from django.db import models

from apps.authentication.models import CustomUser
from apps.journal.models import Tag


class Topic(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='planTopic_images/')
    color = models.CharField(max_length=20)
    description = models.TextField(default='No description provided')

    def __str__(self):
        return self.name


class Activity(models.Model):
    text = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topic.name} - {self.text[:50]}"


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.TextField()
    flag = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.topic.name} - {self.number}"


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DepActivity(models.Model):
    text = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserDepActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.TextField()
    flag = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
