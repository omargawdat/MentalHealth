from django.urls import path

from apps.weekly.views import LifeAspectTypeListView, LifeAspectCreateView

urlpatterns = [
    path('life-aspect-types/', LifeAspectTypeListView.as_view(), name='life-aspect-type-list'),
    path('life-record/', LifeAspectCreateView.as_view(), name='life-aspect-create'),
]
