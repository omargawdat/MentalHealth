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
        fields = ['id', 'name', 'subtopic', 'audio']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['lesson', 'read']


class LessonWithProgressSerializer(serializers.ModelSerializer):
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'subtopic', 'user_progress']

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            try:
                progress = UserProgress.objects.get(user=user, lesson=obj)
            except UserProgress.DoesNotExist:
                progress = None

            # Find the first lesson in the first subtopic of the topic
            first_subtopic = SubTopic.objects.filter(topic=obj.subtopic.topic).order_by('id').first()
            if first_subtopic:
                first_lesson = Lesson.objects.filter(subtopic=first_subtopic).order_by('id').first()
                if first_lesson == obj:
                    if not progress:
                        progress = UserProgress.objects.create(user=user, lesson=obj, read=True)
                    elif not progress.read:
                        progress.read = True
                        progress.save()

            if progress:
                return UserProgressSerializer(progress).data

        return None


class LessonIdSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
