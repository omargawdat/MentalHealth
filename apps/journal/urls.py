from django.urls import include, path


from .views import *




urlpatterns = [
    path('primary-emotions/', PrimaryEmotionList.as_view(), name='primary-emotions-list'),
    path('emotions/', EmotionList.as_view(), name='primary-emotion-list'),
    path('mood-primary-entry/', MoodPrimaryEntryAPIView.as_view(), name='mood-primary-entry-api'),
    path('mood-second-entry/', MoodSecondEntryAPIView.as_view(), name='mood-second-entry-api'),
    path('current-month-moods/', CurrentMonthMoodsAPIView.as_view(), name='current-month-moods-api'),
]
