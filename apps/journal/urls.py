from django.urls import include, path


from .views import *




urlpatterns = [
    path('primary-emotions/', PrimaryEmotionList.as_view(), name='primary-emotions-list'),
    path('emotions/', EmotionList.as_view(), name='primary-emotion-list'),
    path('mood-primary-entry/', MoodPrimaryEntryAPIView.as_view(), name='mood-primary-entry-api'),
    path('mood-second-entry/', MoodSecondEntryAPIView.as_view(), name='mood-second-entry-api'),
    path('current-month-moods/', CurrentMonthMoodsAPIView.as_view(), name='current-month-moods-api'),
    path('journal-entry/', JournalEntryAPIView.as_view(), name='journal-entry-api'),
    path('preference-questions/', PreferenceQuestionListView.as_view(), name='preference-question-list'),
    path('preference-questions/answer/', PreferenceQuestionAnswerView.as_view(), name='preference-question-answer'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('reasons/', ReasonListView.as_view(), name='reason-list'),
    path('activity-entries/', ActivityEntryView.as_view(), name='activity_entries'),
    path('reason-entries/', ReasonEntryView.as_view(), name='reason_entries'),
    path('emotion-count/', EmotionCountView.as_view(), name='emotion_count'),   
    path('activity-count/', ActivityCountView.as_view(), name='activity_count'),
    path('activity-count-this-month/', ActivityCountThisMonthView.as_view(), name='activity_count_this_month'),
    path('report/', Report.as_view(), name='daily_report'),
    path('report-month/', Report2.as_view(), name='daily_report'),
    path('delete-user-input-today/', DeleteUserInputToday.as_view(), name='delete-user-input-today'),
   

]



