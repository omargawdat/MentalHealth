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


# models.py
from django.db import models


class Content(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='content_images/')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    content = models.ForeignKey(Content, related_name='lessons', on_delete=models.CASCADE)
    text_explanation = models.TextField()
    lesson_number = models.IntegerField()

    class Meta:
        ordering = ['lesson_number']

    def __str__(self):
        return f"{self.lesson_number}: {self.text_explanation[:50]}..."  # Show first 50 characters


class LifeOverview(models.Model):
    image = models.ImageField(upload_to='life_overviews/')
    text = models.TextField()

    def __str__(self):
        return f"Life Overview #{self.pk}"  # Using the primary key as a simple identifier


class NegativeThoughtsType(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='negative_thoughts/')
    explanation = models.TextField()
    tip = models.TextField()

    def __str__(self):
        return self.name


class Meditation(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='meditation_images/')
    url = models.URLField()

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='topics/')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class TopicActivity(models.Model):
    topic = models.ForeignKey(Topic, related_name='activities', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag, blank=True)
    activity_text = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.name} Activity #{self.order}"


class DepressionTestQuestion(models.Model):
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question {self.id}: {self.question_text[:50]}"
