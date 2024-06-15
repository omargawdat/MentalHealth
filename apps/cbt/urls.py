# create url patters
from django.urls import path

from apps.cbt.views import NegativeThinkingTypeList, CBTQuestionListByType

urlpatterns = [
    path('negative-thinking-types/', NegativeThinkingTypeList.as_view(), name='negative-thinking-type-list'),
    path('cbt-questions-by-type/', CBTQuestionListByType.as_view(), name='cbt-questions-by-type'),
]
