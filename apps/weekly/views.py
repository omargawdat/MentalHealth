from rest_framework import generics, status
from rest_framework.response import Response

from .models import LifeAspectType
from .serializer import LifeAspectTypeSerializer, LifeAspectSerializer


class LifeAspectCreateView(generics.CreateAPIView):
    serializer_class = LifeAspectSerializer

    def create(self, request, *args, **kwargs):
        aspect_scores = request.data.get('scores', [])
        created_records = []

        for aspect_score in aspect_scores:
            serializer = self.get_serializer(data=aspect_score)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            created_records.append(serializer.data)
 
        return Response(created_records, status=status.HTTP_201_CREATED)


class LifeAspectTypeListView(generics.ListAPIView):
    queryset = LifeAspectType.objects.all()
    serializer_class = LifeAspectTypeSerializer
