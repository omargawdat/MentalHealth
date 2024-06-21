from rest_framework import generics, status
from rest_framework.response import Response
from datetime import date
from .serializers import *
from rest_framework import status
import calendar
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta  
# from .scripts.Dep_test import predict
# from .scripts.Stress_test import predict

from django.shortcuts import get_object_or_404
from datetime import datetime

class PrimaryEmotionList(APIView):
    def get(self, request):
        primary_emotions = Emotion.objects.filter(type="primary")
        serializer = EmotionSerializer(primary_emotions, many=True)
        return Response(serializer.data)
    
class ActivityListView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ReasonListView(generics.ListAPIView):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer     
    
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
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])

        # Retrieve mood entries for the current month
        mood_entries = MoodPrimaryEntry.objects.filter(user=current_user, date__range=(first_day_of_month, last_day_of_month)).order_by('date')

        mood_data = []

        # Iterate over each day of the month
        current_date = first_day_of_month
        while current_date <= last_day_of_month:
            mood_entry = mood_entries.filter(date=current_date).first()

            # If no mood entry exists for the current day, add a special image
            if not mood_entry:
                # Add special image data for days without entries
                mood_data.append({
                    'date': current_date.date(),
                    'mood': None,
                    'emotion_image': '/media/Cream1.png'  
                })
            else:
                # Retrieve the emotion image for the mood entry
                mood = mood_entry.mood
                emotion_instance = Emotion.objects.filter(name=mood, type='primary').first()
                emotion_image_url = emotion_instance.image.url if emotion_instance else None
                
                mood_data.append({
                    'date': current_date.date(),
                    'mood': mood,
                    'emotion_image': emotion_image_url
                })

            # Move to the next day
            current_date += timedelta(days=1)

        return Response(mood_data, status=status.HTTP_200_OK)
        
class JournalEntryAPIView(APIView):
     def post(self, request, *args, **kwargs):
         existing_entry = JournalEntry.objects.filter(user=request.user, date=date.today()).first()
         if existing_entry:
             existing_entry.notes = request.data.get('notes')
#             existing_entry.has_stress = predict(existing_entry.notes)
#             existing_entry.has_depression = predict(existing_entry.notes)
             existing_entry.save()
             serializer = JournalEntrySerializer(existing_entry)
             return Response(serializer.data, status=status.HTTP_200_OK)
         serializer = JournalEntrySerializer(data=request.data)
         if serializer.is_valid():
             journal_entry = serializer.save(user=request.user)
#             journal_entry.has_stress = predict(journal_entry.notes)
#             journal_entry.has_depression = predict(journal_entry.notes)
             journal_entry.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PreferenceQuestionListView(APIView):
    def get(self, request):
        questions = Preference.objects.all()
        serializer = PreferenceSerializer(questions, many=True)
        return Response(serializer.data)
    
class PreferenceQuestionAnswerView(APIView):
    def post(self, request):
        user = request.user
        answers = request.data.get('answers', [])
        yes_tags = [answer['tag'] for answer in answers if answer['answer'] == 'yes']
        # Assuming 'default_tag' is the default tag you want to associate
        yes_tags.append('Default')

        for tag_name in yes_tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            UserTags.objects.create(user=user, tag=tag)

        return Response({'message': 'Answers saved successfully'})
    
class ActivityEntryView(APIView):
    def post(self, request, *args, **kwargs):
        # Get today's date
        today = date.today()

        # Get existing activity entries for today
        existing_entries = ActivityEntry.objects.filter(date=today, user=request.user)

        # Delete existing entries for today
        existing_entries.delete()

        # Create new activity entries
        serializer = ActivityEntrySerializer(data=request.data.get('activities', []), many=True)
        if serializer.is_valid():
            for entry in serializer.validated_data:
                entry['date'] = today
                entry['user'] = request.user
            serializer.save()
            return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ReasonEntryView(APIView):
    def post(self, request, *args, **kwargs):
        # Get today's date
        today = date.today()

        # Get existing reason entries for today
        existing_entries = ReasonEntry.objects.filter(date=today, user=request.user)

        # Delete existing entries for today
        existing_entries.delete()

        # Create new reason entries
        serializer = ReasonEntrySerializer(data=request.data.get('reasons', []), many=True)
        if serializer.is_valid():
            for entry in serializer.validated_data:
                entry['date'] = today
                entry['user'] = request.user
            serializer.save()
            return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmotionCountView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve emotions and their counts for the current user
        user_emotions = (
            MoodPrimaryEntry.objects
            .filter(user=request.user)
            .values('mood')
            .annotate(count=Count('mood'))
        )

        # Serialize the data
        serializer = EmotionCountSerializer(user_emotions, many=True)

        return Response(serializer.data)
    
            
class ActivityCountView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve activities and their counts for the current user
        user_activities = (
            ActivityEntry.objects
            .filter(user=request.user)
            .values('activity')
            .annotate(count=Count('activity'))
        )

        # Serialize the data
        serializer = ActivityCountSerializer(user_activities, many=True)

        return Response(serializer.data)

class ActivityCountThisMonthView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the first and last day of the current month
        today = now()
        first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month + 1) - timedelta(days=1)

        # Retrieve activities and their counts for the current user for this month
        user_activities_this_month = (
            ActivityEntry.objects
            .filter(user=request.user, date__range=[first_day_of_month, last_day_of_month])
            .values('activity')
            .annotate(count=Count('activity'))
        )

        # Serialize the data
        serializer = ActivityCountSerializer(user_activities_this_month, many=True)

        return Response(serializer.data)
    
    
from rest_framework.exceptions import NotFound
import random
class Report(APIView):
    def get(self, request, format=None):
        # Get today's date
        current_datetime = datetime.now()
        date = current_datetime.date()

        user = request.user

        primary_mood_entry = get_object_or_404(MoodPrimaryEntry, user=user, date=date)
        primary_mood_serializer = MoodPrimaryEntrySerializer(primary_mood_entry)

        secondary_mood_entry = MoodSecondEntry.objects.filter(user=user, date=date).first()
        secondary_mood_serializer = MoodSecondEntrySerializer(secondary_mood_entry) if secondary_mood_entry else None

        reason_entries = ReasonEntry.objects.filter(user=user, date=date)
        reason_serializer = ReasonEntrySerializer(reason_entries, many=True) if reason_entries else None

        activity_entries = ActivityEntry.objects.filter(user=user, date=date)
        activity_serializer = ActivityEntrySerializer(activity_entries, many=True) if activity_entries else None

        journal_entry = JournalEntry.objects.filter(user=user, date=date).first()
        journal_serializer = JournalEntrySerializer(journal_entry) if journal_entry else None
        stress_tip = None
        if journal_entry and journal_entry.has_stress:
                stress_tips = TipsStress.objects.all()
                stress_tip = random.choice(stress_tips).description if stress_tips else None

        # Get the primary emotion for the primary mood entry
        primary_emotion = primary_mood_entry.mood
        primary_emotion_instance = Emotion.objects.filter(name=primary_emotion, type='primary').first()
        primary_emotion_image = primary_emotion_instance.image.url if primary_emotion_instance else None

        # Get the secondary emotion for the secondary mood entry
        secondary_emotion = secondary_mood_entry.mood if secondary_mood_entry else None
        secondary_emotion_instance = Emotion.objects.filter(name=secondary_emotion, type='primary').first()
        secondary_emotion_image = secondary_emotion_instance.image.url if secondary_emotion_instance else None
        # Get user's tags
        user_tags = UserTags.objects.filter(user=user)

        # Filter tips based on user's tags and primary emotion
        filtered_tips = Tips.objects.filter(tag__in=user_tags.values_list('tag', flat=True), emotion=primary_emotion)

        # Randomly select a tip
        tip_of_the_day = random.choice(filtered_tips).description if filtered_tips else None

        data = {
            "primary_mood": {
                "mood": primary_mood_serializer.data['mood'],
                "date": primary_mood_serializer.data['date'],
                "emotion_image": primary_emotion_image
            },
            "secondary_mood": {
                "mood": secondary_mood_serializer.data['mood'] if secondary_mood_serializer else None,
                "date": secondary_mood_serializer.data['date'] if secondary_mood_serializer else None,
                
            },
            "reason": reason_serializer.data if reason_serializer else None,
            "activity": activity_serializer.data if activity_serializer else None,
            "note": journal_serializer.data['notes'] if journal_serializer else None,
            "stress_tip": stress_tip,
            "tip_of_the_day": tip_of_the_day
        }

        return Response(data, status=status.HTTP_200_OK)
    
    
from datetime import datetime, timedelta
from calendar import monthrange

class Report2(APIView):
    def get(self, request, format=None):
        # Get the first and last day of the current month
        current_datetime = datetime.now()
        first_day = current_datetime.replace(day=1)
        last_day = current_datetime.replace(day=monthrange(current_datetime.year, current_datetime.month)[1])

        user = request.user

        data = {}
        for i in range((last_day - first_day).days + 1):
            date = first_day + timedelta(days=i)

            primary_mood_entry = MoodPrimaryEntry.objects.filter(user=user, date=date).first()
            secondary_mood_entry = MoodSecondEntry.objects.filter(user=user, date=date).first()
            reason_entries = ReasonEntry.objects.filter(user=user, date=date)
            activity_entries = ActivityEntry.objects.filter(user=user, date=date)
            journal_entry = JournalEntry.objects.filter(user=user, date=date).first()

            # Skip the day if all entries are null except for "tip_of_the_day"
            if not any([primary_mood_entry, secondary_mood_entry, reason_entries, activity_entries, journal_entry]):
                continue

            primary_mood_serializer = MoodPrimaryEntrySerializer(primary_mood_entry) if primary_mood_entry else None
            secondary_mood_serializer = MoodSecondEntrySerializer(secondary_mood_entry) if secondary_mood_entry else None
            reason_serializer = ReasonEntrySerializer(reason_entries, many=True) if reason_entries else None
            activity_serializer = ActivityEntrySerializer(activity_entries, many=True) if activity_entries else None
            journal_serializer = JournalEntrySerializer(journal_entry) if journal_entry else None

            primary_emotion_image = None
            if primary_mood_entry:
                primary_emotion_instance = Emotion.objects.filter(name=primary_mood_entry.mood, type='primary').first()
                if primary_emotion_instance:
                    primary_emotion_image = primary_emotion_instance.image.url

            data[str(date.date())] = {
                "primary_mood": {
                    "mood": primary_mood_serializer.data['mood'] if primary_mood_serializer else None,
                    "date": str(date.date()),
                    "emotion_image": primary_emotion_image
                },
                "secondary_mood": {
                    "mood": secondary_mood_serializer.data['mood'] if secondary_mood_serializer else None,
                    "date": str(date.date())
                },
                "reason": reason_serializer.data if reason_serializer else None,
                "activity": activity_serializer.data if activity_serializer else None,
                "note": journal_serializer.data['notes'] if journal_serializer else None,
              
            }

        return Response(data, status=status.HTTP_200_OK)
    
class DeleteUserInputToday(APIView):
    def delete(self, request):
        user = request.user
        today = date.today()
        # Delete primary mood entry for today
        MoodPrimaryEntry.objects.filter(user=user, date=today).delete()
        # Delete secondary mood entry for today
        MoodSecondEntry.objects.filter(user=user, date=today).delete()
        # Delete journal entry for today
        JournalEntry.objects.filter(user=user, date=today).delete()
        # Delete activity entries for today
        ActivityEntry.objects.filter(user=user, date=today).delete()
        # Delete reason entries for today
        ReasonEntry.objects.filter(user=user, date=today).delete()
        return Response({'message': 'User input for today deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class UserInputListByMonthAPIView(APIView):
    serializer_class = MoodPrimaryEntrySerializer
    def post(self, request):
        # Get the month number from the request body
        month_number = request.data.get('month_number')
        if month_number is None:
            return Response({'error': 'Month number is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the current user
        current_user = self.request.user
        # Get the year and month from the current date
        today = datetime.today()
        year = today.year
        # Validate the month number
        if not 1 <= month_number <= 12:
            return Response({'error': 'Invalid month number'}, status=status.HTTP_400_BAD_REQUEST)
        # Calculate the start and end dates for the specified month
        start_date = datetime(year, month_number, 1).date()
        end_date = start_date + timedelta(days=calendar.monthrange(year, month_number)[1] - 1)
        # Retrieve mood entries for the specified month
        mood_entries = MoodPrimaryEntry.objects.filter(user=current_user, date__range=(start_date, end_date)).order_by('date')
        mood_data = []
        # Iterate over each day of the specified month
        current_date = start_date
        while current_date <= end_date:
            mood_entry = mood_entries.filter(date=current_date).first()
            if mood_entry:
                # If mood entry exists for the current day
                mood = mood_entry.mood
                emotion_instance = Emotion.objects.filter(name=mood, type='primary').first()
                emotion_image_url = emotion_instance.image.url if emotion_instance else None
                mood_data.append({
                    'date': current_date,
                    'mood': mood,
                    'emotion_image': emotion_image_url
                })
            else:
                # If no mood entry exists for the current day, add a special image
                mood_data.append({
                    'date': current_date,
                    'mood': None,
                    'emotion_image': '/media/Cream1.png'
                })
            # Move to the next day
            current_date += timedelta(days=1)
        return Response(mood_data, status=status.HTTP_200_OK)
