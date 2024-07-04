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


class JournalEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notes = models.TextField()
    date = models.DateField(auto_now_add=True)
    has_stress = models.BooleanField(default=True)
    has_depression = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'date')


class ActivityEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)


class ReasonEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_text = models.CharField(max_length=255)
    activity_image = models.ImageField(upload_to='activity_images/', null=True, blank=True)

    def str(self):
        return self.activity_text


class Reason(models.Model):
    reason_id = models.AutoField(primary_key=True)
    reason_text = models.CharField(max_length=255)
    reason_image = models.ImageField(upload_to='reason_images/', null=True, blank=True)

    def str(self):
        return self.reason_text


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Preference(models.Model):
    question_text = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=3, default='yes')
    option2 = models.CharField(max_length=3, default='no')


class UserTags(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Tips(models.Model):
    description = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class TipsStress(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description
