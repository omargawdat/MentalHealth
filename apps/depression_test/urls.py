from django.urls import path

from . import views

urlpatterns = [
    path('test-api-class-view/', views.TestAPIView.as_view(), name='test-api-class-view'),
]
