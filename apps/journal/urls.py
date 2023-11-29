from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'journals', JournalViewSet, basename='journal')

urlpatterns = [
    path('', include(router.urls)),
    path('emotions/', EmotionViewSet.as_view({'get': 'list'})),
    path('emotions-tracker/', UserEmotionHistoryView.as_view(), name='user-emotions'),
]
