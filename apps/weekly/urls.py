from django.urls import path

from apps.weekly.views import LifeAspectTypeListView, LifeAspectCreateView, LifeAspectHistoryView, \
    UncheckedLifeActivityTrackListView, CheckLifeActivityTrackView

urlpatterns = [
    path('life-aspect-types/', LifeAspectTypeListView.as_view(), name='life-aspect-type-list'),
    path('life-record/', LifeAspectCreateView.as_view(), name='life-aspect-create'),
    path('life-record-history/', LifeAspectHistoryView.as_view(), name='life-aspect-history'),
    path('unchecked-activities/', UncheckedLifeActivityTrackListView.as_view(), name='unchecked-activities'),
    path('check-activity/<int:pk>/', CheckLifeActivityTrackView.as_view(), name='check-activity'),
]
