from django.db import models

from apps.authentication.models import CustomUser


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    pic = models.ImageField(upload_to='topic_pics/', blank=True, null=True)

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    subtopic = models.ForeignKey(SubTopic, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.lesson.name}"
