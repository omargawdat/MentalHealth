from django.db.models import DateField, Avg
from django.db.models.functions import Trunc
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import LifeAspect
from .models import LifeAspectType
from .serializer import LifeAspectHistorySerializer
from .serializer import LifeAspectTypeSerializer, LifeAspectSerializer


class LifeAspectTypeListView(generics.ListAPIView):
    queryset = LifeAspectType.objects.all()
    serializer_class = LifeAspectTypeSerializer


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


class LifeAspectHistoryView(generics.ListAPIView):
    serializer_class = LifeAspectHistorySerializer

    def get_queryset(self):
        return LifeAspect.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.annotate(day=Trunc('date', 'day', output_field=DateField())).values('day',
                                                                                                'aspect_type__name').annotate(
            avg_value=Avg('value')).order_by('day', 'aspect_type__name')

        grouped_data = {}

        for item in queryset:
            day = item['day'].strftime('%Y-%m-%d')
            aspect_type = item['aspect_type__name']
            avg_value = item['avg_value']

            if day not in grouped_data:
                grouped_data[day] = []

            grouped_data[day].append({
                'aspect_type': aspect_type,
                'value': avg_value
            })

        # Check if the last record was 7 days ago
        last_record = self.get_queryset().order_by('-date').first()
        last_record_7_days_ago = False

        if last_record:
            last_record_date = last_record.date
            seven_days_ago = timezone.now().date() - timezone.timedelta(days=7)
            last_record_7_days_ago = last_record_date <= seven_days_ago

        response_data = {
            'is_7_days_ago': last_record_7_days_ago,
            'history': grouped_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
