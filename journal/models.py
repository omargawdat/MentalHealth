
from django.db import models
from django.utils import timezone
from apps.authentication.models import CustomUser




# Create your models here.
class jornalentry(models.Model):
   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)

   