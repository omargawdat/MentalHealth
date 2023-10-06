from django.db import models

from apps.authentication.models import CustomUser


class Journal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
