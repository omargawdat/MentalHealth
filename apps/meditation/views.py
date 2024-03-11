from rest_framework import generics
from .models import Meditation
from .serializer import MeditationSerializer


class MeditationListCreate(generics.ListAPIView):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer
    permission_classes = []
