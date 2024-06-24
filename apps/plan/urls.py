from django.urls import path
from .views import FirstFalseUserActivityView, FlagActivityView, TopicListView, TopicActivityView, ActivityTextView, RestartTopicView

urlpatterns = [
    path('plan/topics/', TopicListView.as_view(), name='topic-list'),
    path('plan/topic-activities/', TopicActivityView.as_view(), name='topic-activities'),
    path('plan/activity-text/', ActivityTextView.as_view(), name='activity-text'),
    path('plan/restart-topic/', RestartTopicView.as_view(), name='restart-topic'),
    path('first-false-user-activity/', FirstFalseUserActivityView.as_view(), name='first_false_user_activity'),
    path('flag-activity/', FlagActivityView.as_view(), name='flag_activity'),
]

