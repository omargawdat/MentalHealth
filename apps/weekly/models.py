from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.authentication.models import CustomUser


class LifeAspectType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LifeAspect(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    aspect_type = models.ForeignKey(LifeAspectType, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.aspect_type.name}: {self.value}"


class LifeActivity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    aspect_type = models.ForeignKey(LifeAspectType, on_delete=models.CASCADE, related_name='activities')

    def __str__(self):
        return self.name


class LifeActivityTrack(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_tracks')
    life_activity = models.ForeignKey(LifeActivity, on_delete=models.CASCADE, related_name='activity_tracks')
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)
