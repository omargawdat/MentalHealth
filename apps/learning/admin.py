from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Topic, SubTopic, Lesson, UserProgress


class SubTopicInline(TabularInline):
    model = SubTopic
    extra = 1
    show_change_link = True


class LessonInline(TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ['name', 'subtopic_count', 'has_picture']
    search_fields = ['name']
    inlines = [SubTopicInline]

    @display(description=_("Subtopics"), ordering="subtopic_count")
    def subtopic_count(self, obj):
        return obj.subtopic_count

    @display(boolean=True, description=_("Has Picture"))
    def has_picture(self, obj):
        return bool(obj.pic)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            subtopic_count=Count('subtopics', distinct=True)
        )


@admin.register(SubTopic)
class SubTopicAdmin(ModelAdmin):
    list_display = ['name', 'topic', 'lesson_count']
    list_filter = ['topic']
    search_fields = ['name', 'topic__name']
    autocomplete_fields = ['topic']
    inlines = [LessonInline]

    @display(description=_("Lessons"), ordering="lesson_count")
    def lesson_count(self, obj):
        return obj.lesson_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            lesson_count=Count('lessons', distinct=True)
        )


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ['name', 'subtopic', 'content_preview', 'progress_count']
    list_filter = ['subtopic__topic', 'subtopic']
    search_fields = ['name', 'content', 'subtopic__name', 'subtopic__topic__name']
    autocomplete_fields = ['subtopic']
    
    @display(description=_("Content Preview"))
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    @display(description=_("User Progress"), ordering="progress_count")
    def progress_count(self, obj):
        return obj.progress_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            progress_count=Count('userprogress', distinct=True)
        )


@admin.register(UserProgress)
class UserProgressAdmin(ModelAdmin):
    list_display = ['user', 'lesson', 'read']
    list_filter = ['read', 'lesson__subtopic__topic', 'lesson__subtopic']
    search_fields = ['user__email', 'lesson__name']
    autocomplete_fields = ['lesson']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'lesson', 'lesson__subtopic',
                                                            'lesson__subtopic__topic')
