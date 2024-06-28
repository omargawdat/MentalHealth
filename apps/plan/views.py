from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.depression_test.models import DepressionTestAttempt
from .models import DepActivity, Topic, Activity, UserActivity, UserDepActivity
from apps.journal.models import Tag, UserTags,JournalEntry
from .serializers import ActivityNumberSerializer, DepActivitySerializer, TopicSerializer
import random



class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


def randomize_activities(topic, user):
    user_tags = UserTags.objects.filter(user=user).values_list('tag', flat=True)
    if not user_tags.exists():
        return [], False

    activities = Activity.objects.filter(topic=topic, tag__in=user_tags)
    if not activities.exists():
        return [], False

    # Clear existing UserActivity entries for the topic and user
    UserActivity.objects.filter(user=user, topic=topic).delete()

    random_activities = random.sample(list(activities), min(len(activities), 21))
    user_activities = []

    for activity in random_activities:
        if not activity.text:
            print(f"Empty text found for activity: {activity.id}")

    for index, activity in enumerate(random_activities, start=1):
        user_activity = UserActivity(
            user=user,
            topic=topic,
            tag=activity.tag,
            number=index,
            text=activity.text,  # Ensure text is assigned correctly
            flag=False
        )
        user_activities.append(user_activity)

    UserActivity.objects.bulk_create(user_activities)

    # Return the randomized activities and success flag
    return random_activities, True




class TopicActivityView(APIView):
    def post(self, request):
        topic_name = request.data.get('topic_name')
        if not topic_name:
            return Response({'detail': 'Topic name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the topic
        topic = get_object_or_404(Topic, name=topic_name)
        topic_serializer = TopicSerializer(topic).data
        # Retrieve user's tags
        user = request.user  # Assuming user is authenticated
        user_tags = UserTags.objects.filter(user=user).values_list('tag', flat=True)
        if not user_tags.exists():
            return Response({'detail': 'No tags found for the user.'}, status=status.HTTP_404_NOT_FOUND)
        # Check if the user already has activities planned for this topic
        user_activities = UserActivity.objects.filter(user=user, topic=topic)
        if user_activities.exists():
            # Use the planned activities and sort them by number
            activities = [{'number': activity.number, 'flag': activity.flag} for activity in user_activities.order_by('number')]
        else:
            # Randomize activities and save to UserActivity model
            activities, success = randomize_activities(topic, user)
            if not success:
                return Response({'detail': 'No activities found related to this topic and user tags.'}, status=status.HTTP_404_NOT_FOUND)
            # Use the random activities
            activities = [{'number': i + 1, 'flag': False} for i, _ in enumerate(activities)]
        return Response({
            'topic': topic_serializer,
            'activities': activities
        }, status=status.HTTP_200_OK)




class ActivityTextView(APIView):
    def post(self, request):
        number = request.data.get('number')
        topic_name = request.data.get('topic_name')
        if not number or not topic_name:
            return Response({'detail': 'Number and topic name are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the topic
        topic = get_object_or_404(Topic, name=topic_name)
        # Retrieve the activity text from UserActivity model
        try:
            user_activity = UserActivity.objects.get(user=request.user, topic=topic, number=number)
        except UserActivity.DoesNotExist:
            return Response({'detail': 'No activity found for the given number.'}, status=status.HTTP_404_NOT_FOUND)
        user_activity.save()
        return Response({'number': number, 'text': user_activity.text}, status=status.HTTP_200_OK)
    

class RestartTopicView(APIView):
    def post(self, request):
        topic_name = request.data.get('topic_name')
        if not topic_name:
            return Response({'detail': 'Topic name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the topic
        topic = get_object_or_404(Topic, name=topic_name)
        # Check if user already has activities for this topic
        user = request.user
        user_activities_exist = UserActivity.objects.filter(user=user, topic=topic).exists()
        # If activities exist, delete them
        if user_activities_exist:
            UserActivity.objects.filter(user=user, topic=topic).delete()
        # Randomize activities and set flags again
        activities, success = randomize_activities(topic, user)
        if not success:
            return Response({'detail': 'No activities found related to this topic and user tags.'}, status=status.HTTP_404_NOT_FOUND)
        # Construct response with randomized activities
        numbered_activities = [{'number': i, 'flag': False} for i in range(1, 22)]
        return Response({
            'topic': {
                'id': topic.id,
                'name': topic.name,
                'color': topic.color,
                'image': topic.image.url  
            },
            'activities': numbered_activities
        }, status=status.HTTP_200_OK)



class FirstFalseUserActivityView(APIView):
    def get(self, request):
        user = request.user  
        topics = Topic.objects.all()
        first_false_activities = []
        for topic in topics:
            first_false_activity = UserActivity.objects.filter(user=user, topic=topic, flag=False).order_by('number').first()
            if first_false_activity:
                first_false_activities.append({
                    'topic': TopicSerializer(topic).data,
                    'activity': {
                        'number': first_false_activity.number,
                        'text': first_false_activity.text,
                        'flag': first_false_activity.flag
                    }
                })
        return Response({
            'first_false_activities': first_false_activities
        }, status=status.HTTP_200_OK)
    

class FlagActivityView(APIView):
    def post(self, request):
        topic_name = request.data.get('topic_name')
        activity_number = request.data.get('activity_number')
        if not topic_name or not activity_number:
            return Response({'detail': 'Topic name and activity number are required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the topic
        topic = get_object_or_404(Topic, name=topic_name)
        # Retrieve the user
        user = request.user
        # Retrieve the user activity to flag
        try:
            user_activity = UserActivity.objects.get(user=user, topic=topic, number=activity_number)
        except UserActivity.DoesNotExist:
            return Response({'detail': 'No activity found for the given topic and number.'}, status=status.HTTP_404_NOT_FOUND)
        # Mark the activity as flagged
        user_activity.flag = True
        user_activity.save()
        # Prepare response
        response_data = {
            'topic': TopicSerializer(topic).data,
            'activity': {
                'number': user_activity.number,
                'text': user_activity.text,
                'flag': user_activity.flag
            }
        }
        return Response(response_data, status=status.HTTP_200_OK,)
    

class CheckDepressionStreakView(APIView):
    def get(self, request):
        user = request.user  
        # Calculate the date range for the past 15 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=14)  # 15 days including today
        # Query JournalEntry entries for the user within the date range
        entries = JournalEntry.objects.filter(user=user, date__range=[start_date, end_date])
        # Ensure there are exactly 15 entries
        if entries.count() != 15:
            return Response({'depression_streak': False}, status=status.HTTP_200_OK)
        # Ensure all entries indicate depression
        all_depression = all(entry.has_depression for entry in entries)
        return Response({'depression_streak': all_depression}, status=status.HTTP_200_OK)
    


# Helper function to randomize activities and save to UserDepActivity model
def get_user_depression_activities(user):
    # Retrieve the most recent depression level
    depression_test_attempt = DepressionTestAttempt.objects.filter(user=user).order_by('-timestamp').first()
    if not depression_test_attempt:
        return None, 'No depression test attempt found for the user.'
    level_of_depression = depression_test_attempt.level_of_depression
    # Retrieve user's tags
    user_tags = UserTags.objects.filter(user=user).values_list('tag', flat=True)
    if not user_tags.exists():
        return None, 'No tags found for the user.'
    # Retrieve activities related to the user's tags and level of depression
    activities = DepActivity.objects.filter(tag__in=user_tags, level__name=level_of_depression)
    if not activities.exists():
        return None, level_of_depression
    # Randomize and select up to 21 activities
    random_activities = random.sample(list(activities), min(len(activities), 21))
    # Clear previous user activities for this level
    UserDepActivity.objects.filter(user=user, level__name=level_of_depression).delete()
    # Save the randomized activities to UserDepActivity model
    user_activities = []
    for index, activity in enumerate(random_activities, start=1):
        user_activity = UserDepActivity(
            user=user, 
            level=activity.level,
            tag=activity.tag,
            number=index,
            text=activity.text,
            flag=False
        )
        user_activities.append(user_activity)
    UserDepActivity.objects.bulk_create(user_activities)
    # Serialize the activities
    activities_serializer = DepActivitySerializer(random_activities, many=True)
    return activities_serializer.data, None


# API view to generate and get user depression activities
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_depression_activities(request):
    user = request.user
    # Call function to generate and save new activities
    activities, error = get_user_depression_activities(user)
    if error:
        return Response({'detail': error}, status=status.HTTP_404_NOT_FOUND)
    return Response({'activities': activities}, status=status.HTTP_200_OK)

# API view to change the flag of an activity to true
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flag_depression_activity(request):
    serializer = ActivityNumberSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    number = serializer.validated_data['number']
    user = request.user
    # Retrieve the most recent depression level
    depression_test_attempt = DepressionTestAttempt.objects.filter(user=user).order_by('-timestamp').first()
    if not depression_test_attempt:
        return Response({'detail': 'No depression test attempt found for the user.'}, status=status.HTTP_404_NOT_FOUND)
    level_of_depression = depression_test_attempt.level_of_depression
    # Retrieve the activity from UserDepActivity model
    try:
        activity = UserDepActivity.objects.get(user=user, level__name=level_of_depression, number=number)
    except UserDepActivity.DoesNotExist:
        return Response({'detail': 'No activity found for the given number and depression level.'}, status=status.HTTP_404_NOT_FOUND)
    # Set the flag to true
    activity.flag = True
    activity.save()
    return Response({'detail': 'Activity flagged successfully.'}, status=status.HTTP_200_OK)

# API view to get the first activity with flag=False
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_first_unflagged_activity(request):
    user = request.user
    # Retrieve the most recent depression level
    depression_test_attempt = DepressionTestAttempt.objects.filter(user=user).order_by('-timestamp').first()
    if not depression_test_attempt:
        return Response({'detail': 'No depression test attempt found for the user.'}, status=status.HTTP_404_NOT_FOUND)
    level_of_depression = depression_test_attempt.level_of_depression
    # Check if there are any activities in UserDepActivity
    if not UserDepActivity.objects.filter(user=user, level__name=level_of_depression).exists():
        # Call function to generate and save new activities
        activities, error = get_user_depression_activities(user)
        if error:
            return Response({'detail': error}, status=status.HTTP_404_NOT_FOUND)
    # Retrieve the first activity from UserDepActivity model with flag=False
    activity = UserDepActivity.objects.filter(user=user, level__name=level_of_depression, flag=False).order_by('number').first()
    if not activity:
        return Response({'detail': 'No unflagged activity found for the user and depression level.', 'level_depression': level_of_depression}, status=status.HTTP_404_NOT_FOUND)
    # Check if this is the last unflagged activity
    remaining_unflagged_count = UserDepActivity.objects.filter(user=user, level__name=level_of_depression, flag=False).count()
    if remaining_unflagged_count == 1:
        return Response({
            'number': activity.number,
            'text': activity.text,
            'flag': activity.flag,
            'message': 'This is the last unflagged activity. Please take the depression test again.'
        }, status=status.HTTP_200_OK)
    return Response({'number': activity.number, 'text': activity.text, 'flag': activity.flag}, status=status.HTTP_200_OK)
