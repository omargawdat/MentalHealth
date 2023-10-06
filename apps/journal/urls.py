from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import JournalViewSet

router = DefaultRouter()
router.register(r'journals', JournalViewSet, basename='journal')

urlpatterns = [
    path('', include(router.urls)),
]
