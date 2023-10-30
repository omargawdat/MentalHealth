from django.urls import path

from .views import AnswerOptionListView, CalculateTestView, TestQuestionListView

urlpatterns = [
    path('depression/test_result/', CalculateTestView.as_view(), name='sum_numbers'),
    path('depression/questions/', TestQuestionListView.as_view(), name='test_questions_list'),
    path('depression/answers/', AnswerOptionListView.as_view(), name='answer_options_list'),
]
