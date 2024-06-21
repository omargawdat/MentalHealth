from django.urls import path
from .views import LessonContentView, TopicListView, SubTopicListView, LessonListView

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/subtopics/', SubTopicListView.as_view(), name='subtopic-list'),
    path('subtopics/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/', LessonContentView.as_view(), name='lesson-content'),
    ]