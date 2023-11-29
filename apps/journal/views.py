from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import *
from .serializers import EmotionHistorySerializer


class JournalViewSet(viewsets.ModelViewSet):
    serializer_class = JournalSerializer

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmotionViewSet(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = EmotionSerializer
    queryset = Emotion.objects.filter(parent=None)


class UserEmotionHistoryView(generics.ListCreateAPIView):
    serializer_class = EmotionHistorySerializer

    def get_queryset(self):
        return EmotionHistory.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = request.user
        emotion_id = request.data.get('emotion')
        emotion = get_object_or_404(Emotion, pk=emotion_id)
        date = request.data.get('date', timezone.now().date())

        user_emotion, created = EmotionHistory.objects.update_or_create(
            user=user, date=date,
            defaults={'emotion': emotion}
        )

        serializer = self.serializer_class(user_emotion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
