from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class LifeAspectType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LifeAspect(models.Model):
    aspect_type = models.ForeignKey(LifeAspectType, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aspect_type.name}: {self.value}"
