from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'journals', JournalViewSet, basename='journal')

urlpatterns = [
    path('', include(router.urls)),
    path('primary-emotions/', PrimaryEmotionList.as_view(), name='primary-emotions-list'),
    path('emotions/', EmotionList.as_view(), name='primary-emotion-list'),
    path('mood-primary-entry/', MoodPrimaryEntryAPIView.as_view(), name='mood-primary-entry-api'),
    path('mood-third-entry/', MoodThirdEntryAPIView.as_view(), name='mood-third-entry-api'),
    path('current-month-moods/', CurrentMonthMoodsAPIView.as_view(), name='current-month-moods-api'),
    
]
