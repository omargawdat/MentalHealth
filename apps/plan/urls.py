from django.urls import path
from .views import CheckDepressionStreakView,get_depression_activities, get_first_unflagged_activity,FirstFalseUserActivityView, FlagActivityView, TopicListView, TopicActivityView, ActivityTextView, RestartTopicView, flag_depression_activity

urlpatterns = [
    path('plan/topics/', TopicListView.as_view(), name='topic-list'),
    path('plan/topic-activities/', TopicActivityView.as_view(), name='topic-activities'),
    path('plan/activity-text/', ActivityTextView.as_view(), name='activity-text'),
    path('plan/restart-topic/', RestartTopicView.as_view(), name='restart-topic'),
    path('first-false-user-activity/', FirstFalseUserActivityView.as_view(), name='first_false_user_activity'),
    path('flag-activity/', FlagActivityView.as_view(), name='flag_activity'),
    path('consecutive-depression-check/', CheckDepressionStreakView.as_view(), name='consecutive-depression-check'),
    path('flag-depression-activity/', flag_depression_activity, name='flag_depression_activity'),
    path('dep_first-unflagged-activity/', get_first_unflagged_activity, name='get_first_unflagged_activity'),
    path('get-depression-activity/', get_depression_activities, name='get_depression_activity_by_number'),
]
