from time import timezone
from datetime import datetime, date
from rest_framework import viewsets
import calendar
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics

# class PrimaryEmotionList(APIView):
#     def get(self, request):
#         primary_emotions = Emotion.objects.filter(type="primary")
#         serializer = EmotionSerializer(primary_emotions, many=True)
#         return Response(serializer.data)


class JournalViewSet(viewsets.ModelViewSet):
    serializer_class = JournalSerializer

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

# class EmotionList(APIView):
#     def post(self, request):
#         filter_serializer = FilterSerializer(data=request.data)
#         if filter_serializer.is_valid():
#             filter_data = filter_serializer.validated_data
#             primary_emotions = Emotion.objects.filter(type=filter_data['type'])
#             serializer = EmotionSerializer(primary_emotions, many=True)
#             return Response(serializer.data)
#         return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class MoodPrimaryEntryAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = MoodPrimaryEntrySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# class MoodThirdEntryAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = MoodThirdEntrySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
    
# class CurrentMonthMoodsAPIView(APIView):
#     serializer_class = MoodPrimaryEntrySerializer

#     def get(self, request, *args, **kwargs):
#         current_user =self.request.user
        
#         today = date.today()
#         current_month = today.month
#         current_year = today.year
#         first_day_of_month = date(today.year, today.month, 1)
#         last_day_of_month = date(today.year, today.month, 1)
#         num_days_in_current_month = calendar.monthrange(current_year, current_month)[1]
#         last_day_of_month = last_day_of_month.replace(day=num_days_in_current_month)
       

#         moods = MoodPrimaryEntry.objects.filter(user=current_user,date__range=(first_day_of_month, last_day_of_month))

#         if moods.exists():
#             serializer = self.serializer_class(moods, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "None"}, status=status.HTTP_200_OK)
class StressLevelView(APIView):
    def get(self, request):
        stress_levels = StressLevel.objects.all()
        serializer = StressLevelSerializer(stress_levels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StressLevelEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)