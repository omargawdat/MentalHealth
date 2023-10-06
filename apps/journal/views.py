from rest_framework import viewsets

from .models import Journal
from .serializers import JournalSerializer


class JournalViewSet(viewsets.ModelViewSet):
    serializer_class = JournalSerializer

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
