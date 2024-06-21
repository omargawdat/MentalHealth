from rest_framework import serializers
from .models import Topic, SubTopic, Lesson, UserProgress

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'pic']

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ['id', 'name', 'topic']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name',  'subtopic']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['user', 'lesson', 'read']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = [ 'lesson', 'read']

class LessonWithProgressSerializer(serializers.ModelSerializer):
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name',  'subtopic', 'user_progress']

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                user = request.user
                progress = UserProgress.objects.get(user=user, lesson=obj)
                if not progress.read:
                    # Check if this is the first lesson for the user
                    first_lesson = Lesson.objects.filter(subtopic=obj.subtopic).order_by('id').first()
                    if first_lesson == obj:
                        progress.read = True
                        progress.save()
                return UserProgressSerializer(progress).data
            except UserProgress.DoesNotExist:
                # If there's no progress, create a new one for the user
                first_lesson = Lesson.objects.filter(subtopic=obj.subtopic).order_by('id').first()
                if first_lesson == obj:
                    progress = UserProgress.objects.create(user=user, lesson=obj, read=True)
                    return UserProgressSerializer(progress).data
        return None

class LessonIdSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()