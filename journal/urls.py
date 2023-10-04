from django.urls import path
from django.urls import path
from .views import JournalEntryListCreateView, JournalEntryRetrieveUpdateDestroyView

from . import views
#to get enteries of specific user http://127.0.0.1:8000/api/user/1/entries/
# to get all enteries of all users or create new entery http://127.0.0.1:8000/api/entries/
# to delete or update or view an entery http://127.0.0.1:8000/api/entries/2/
urlpatterns = [
    # path('test/', views.TestAPIView.as_view(), name='test-api-class-view'),
    path('entries/', JournalEntryListCreateView.as_view(), name='entry-list-create'),
    path('entries/<int:pk>/', JournalEntryRetrieveUpdateDestroyView.as_view(), name='entry-detail'),
    path('user/<int:user_id>/entries/', views.get_journal_entries_by_user_id, name='api_journal_entries_by_user'),
]
