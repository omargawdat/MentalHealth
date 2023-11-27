from django.db import models

from apps.authentication.models import CustomUser


class Journal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)

# class Emotion(models.Model):
#     name = models.CharField(max_length=100)
#     type = models.CharField(max_length=50)

#     def str(self):
#         return self.name
    
# class MoodPrimaryEntry(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     mood = models.TextField()
#     date = models.DateField(auto_now_add=True)

# class MoodThirdEntry(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     mood = models.TextField()
#     date = models.DateField(auto_now_add=True)
class StressLevel(models.Model):
       level = models.CharField(max_length=50)
       def __str__(self):
            return self.level
class StressLevelEntry(models.Model):
       user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
       level = models.CharField(max_length=50)
       date = models.DateField(auto_now_add=True)

       def __str__(self):
            return self.level
        
