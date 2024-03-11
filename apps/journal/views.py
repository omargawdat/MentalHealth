from rest_framework import generics, status
from rest_framework.response import Response
from datetime import date
from .serializers import *
from rest_framework import status
import calendar
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class PrimaryEmotionList(APIView):
    def get(self, request):
        primary_emotions = Emotion.objects.filter(type="primary")
        serializer = EmotionSerializer(primary_emotions, many=True)
        return Response(serializer.data)


class EmotionList(APIView):
    def post(self, request):
        filter_serializer = FilterSerializer(data=request.data)
        if filter_serializer.is_valid():
            filter_data = filter_serializer.validated_data
            primary_emotions = Emotion.objects.filter(type=filter_data['type'])
            serializer = SubEmotionSerializer(primary_emotions, many=True)
            return Response(serializer.data)
        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodPrimaryEntryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if mood entry already exists for the current user and date
        existing_entry = MoodPrimaryEntry.objects.filter(user=request.user, date=date.today()).first()
        if existing_entry:
            # Update the existing entry with the new mood
            existing_entry.mood = request.data.get('mood')
            existing_entry.save()
            serializer = MoodPrimaryEntrySerializer(existing_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If no existing entry, create a new entry
        serializer = MoodPrimaryEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoodSecondEntryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Check if mood entry already exists for the current user and date
        existing_entry = MoodSecondEntry.objects.filter(user=request.user, date=date.today()).first()
        if existing_entry:
            # Update the existing entry with the new mood
            existing_entry.mood = request.data.get('mood')
            existing_entry.save()
            serializer = MoodSecondEntrySerializer(existing_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If no existing entry, create a new entry
        serializer = MoodSecondEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentMonthMoodsAPIView(APIView):
    serializer_class = MoodPrimaryEntrySerializer

    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)
        last_day_of_month = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
        moods = MoodPrimaryEntry.objects.filter(user=current_user, date__range=(first_day_of_month, last_day_of_month))
        if moods.exists():
            serializer = self.serializer_class(moods, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "None"}, status=status.HTTP_200_OK)
