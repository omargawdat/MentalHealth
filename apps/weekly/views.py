from django.db.models import DateField, Avg
from django.db.models.functions import Trunc
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LifeAspect, LifeActivity, LifeActivityTrack
from .models import LifeAspectType
from .serializer import LifeAspectHistorySerializer, LifeActivityTrackSerializer
from .serializer import LifeAspectTypeSerializer, LifeAspectSerializer


class LifeAspectTypeListView(generics.ListAPIView):
    queryset = LifeAspectType.objects.all()
    serializer_class = LifeAspectTypeSerializer


class LifeAspectCreateView(generics.CreateAPIView):
    serializer_class = LifeAspectSerializer

    def create(self, request, *args, **kwargs):
        aspect_scores = request.data.get('scores', [])
        created_records = []
        added_activities = []

        for aspect_score in aspect_scores:
            serializer = self.get_serializer(data=aspect_score)
            serializer.is_valid(raise_exception=True)
            life_aspect = serializer.save(user=request.user)
            if life_aspect.value < 3:
                activities = self.add_needed_activities(life_aspect, request.user, num_activities=2)
                added_activities.extend(activities)
            elif life_aspect.value < 6:
                activities = self.add_needed_activities(life_aspect, request.user, num_activities=1)
                added_activities.extend(activities)
            created_records.append(serializer.data)

        response_data = {
            "created_records": created_records,
            "added_activities": LifeActivityTrackSerializer(added_activities, many=True).data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def add_needed_activities(self, life_aspect, user, num_activities):
        activities = LifeActivity.objects.filter(aspect_type=life_aspect.aspect_type)[:num_activities]
        added_activities = []
        for activity in activities:
            activity_track = LifeActivityTrack.objects.create(user=user, life_activity=activity)
            added_activities.append(activity_track)
        return added_activities


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


class UncheckedLifeActivityTrackListView(generics.ListAPIView):
    serializer_class = LifeActivityTrackSerializer

    def get_queryset(self):
        user = self.request.user
        return LifeActivityTrack.objects.filter(user=user, is_checked=False)


class CheckLifeActivityTrackView(APIView):

    def patch(self, request, pk, *args, **kwargs):
        try:
            activity_track = LifeActivityTrack.objects.get(pk=pk, user=request.user)
            activity_track.is_checked = True
            activity_track.save()
            return Response({"detail": "Activity marked as done."}, status=status.HTTP_200_OK)
        except LifeActivityTrack.DoesNotExist:
            return Response({"detail": "Not found or you do not have permission to perform this action."},
                            status=status.HTTP_404_NOT_FOUND)
