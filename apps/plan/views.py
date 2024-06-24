from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Topic, Activity, UserActivity
from apps.journal.models import Tag, UserTags
from .serializers import TopicSerializer, ActivitySerializer, UserActivitySerializer
import random


class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

def randomize_activities(topic, user):
    # Retrieve user's tags
    user_tags = UserTags.objects.filter(user=user).values_list('tag', flat=True)
    if not user_tags.exists():
        return [], False
    # Retrieve activities related to the topic and user's tags
    activities = Activity.objects.filter(topic=topic, tag__in=user_tags)
    if not activities.exists():
        return [], False
    # Clear previous user activities for this topic
    UserActivity.objects.filter(user=user, topic=topic).delete()
    # Randomize activities and set flag=False for each activity
    random_activities = random.sample(list(activities), min(len(activities), 21))
    user_activities = []
    for index, activity in enumerate(random_activities, start=1):
        user_activity = UserActivity(
            user=user, 
            topic=topic, 
            tag=activity.tag,
            number=index,  # Assign sequential numbers from 1 to 21
            text=activity.text, 
            flag=False
        )
        user_activities.append(user_activity)
    UserActivity.objects.bulk_create(user_activities)
    return random_activities, True  # Return only the random activities



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
            # Retrieve activities related to the topic and user's tags
            activities = Activity.objects.filter(topic=topic, tag__in=user_tags)
            if not activities.exists():
                return Response({'detail': 'No activities found related to this topic and user tags.'}, status=status.HTTP_404_NOT_FOUND)
            # Generate random 21 activities
            random_activities = random.sample(list(activities), min(len(activities), 21))
            # Save activities to UserActivity model
            UserActivity.objects.filter(user=user, topic=topic).delete()  # Clear previous entries
            user_activities = []
            for idx, activity in enumerate(random_activities, start=1):
                user_activity = UserActivity(
                    user=user, topic=topic, tag=activity.tag,
                    number=idx, flag=False  # Set flag to False initially
                )
                user_activities.append(user_activity)
            UserActivity.objects.bulk_create(user_activities)
            # Use the random activities
            activities = [{'number': i + 1, 'flag': False} for i, activity in enumerate(random_activities)]
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