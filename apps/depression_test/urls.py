from django.urls import path

from . import views
from .views import TestQuestionAPIView

urlpatterns = [
    path('testu/', views.TestAPIView.as_view(), name='test-api-class-view'),
    path('questions/', TestQuestionAPIView.as_view(), name='test_questions_api'),
    path('calculate-depression-score/', views.calculate_depression_score, name='calculate_depression_score'),
]
