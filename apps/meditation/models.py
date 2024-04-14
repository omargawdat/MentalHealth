from django.db import models


class Meditation(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    url = models.URLField(max_length=200)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name
