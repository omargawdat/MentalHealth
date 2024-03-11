from django.db import models


class Meditation(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='meditations/')
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
