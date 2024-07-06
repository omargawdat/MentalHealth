from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from MentalHealth.settings.common import MEDIA_URL
from .serializers import *


class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class SubTopicListView(APIView):
    def post(self, request, *args, **kwargs):
        topic_id = request.data.get('topic_id')
        if not topic_id:
            return Response({"error": "topic_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)

        subtopics = SubTopic.objects.filter(topic_id=topic_id)
        subtopic_serializer = SubTopicSerializer(subtopics, many=True)
        topic_serializer = TopicSerializer(topic)

        return Response({
            "topic": topic_serializer.data,
            "subtopics": subtopic_serializer.data
        })


class LessonListView(APIView):
    def post(self, request, *args, **kwargs):
        subtopic_id = request.data.get('subtopic_id')
        if not subtopic_id:
            return Response({"error": "subtopic_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        lessons = Lesson.objects.filter(subtopic_id=subtopic_id)
        serializer = LessonWithProgressSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)


class LessonContentView(APIView):
    def post(self, request):
        serializer = LessonIdSerializer(data=request.data)
        if serializer.is_valid():
            lesson_id = serializer.validated_data['lesson_id']
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                user = request.user  # Assuming the user is authenticated
                # Update user progress for the current lesson
                UserProgress.objects.update_or_create(
                    user=user,
                    lesson_id=lesson_id,
                    defaults={'read': True}
                )
                # Check if this is the last lesson in the subtopic
                last_lesson_in_subtopic = Lesson.objects.filter(subtopic=lesson.subtopic).order_by('-id').first()
                if last_lesson_in_subtopic and lesson.id == last_lesson_in_subtopic.id:
                    # Find the next subtopic
                    next_subtopic = SubTopic.objects.filter(topic=lesson.subtopic.topic,
                                                            id__gt=lesson.subtopic.id).order_by('id').first()
                    if next_subtopic:
                        # Find the first lesson in the next subtopic
                        first_lesson_in_next_subtopic = Lesson.objects.filter(subtopic=next_subtopic).order_by(
                            'id').first()
                        if first_lesson_in_next_subtopic:
                            UserProgress.objects.update_or_create(
                                user=user,
                                lesson_id=first_lesson_in_next_subtopic.id,
                                defaults={'read': True}
                            )
                # Find the next lesson in the same subtopic
                else:
                    next_lesson = Lesson.objects.filter(subtopic=lesson.subtopic, id__gt=lesson.id).order_by(
                        'id').first()
                    if next_lesson:
                        UserProgress.objects.update_or_create(
                            user=user,
                            lesson_id=next_lesson.id,
                            defaults={'read': True}
                        )

                audio_url = None
                if lesson.audio:
                    audio_url = request.build_absolute_uri(MEDIA_URL + lesson.audio.name)

                return Response({
                    'content': lesson.content,
                    "audio": audio_url
                })
            except Lesson.DoesNotExist:
                return Response({'message': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
