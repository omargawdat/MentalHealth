from django.urls import path
from .views import MeditationListCreate

urlpatterns = [
    path('meditations/', MeditationListCreate.as_view(), name='meditation-list-create'),
]
