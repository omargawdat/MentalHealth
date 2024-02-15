from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import *
from .models import Meditation, NegativeThoughtsType
from .models import Topic, TopicActivity


class ActivityAdmin(ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)

    image_tag.short_description = 'Image'


class ReasonAdmin(ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)

    image_tag.short_description = 'Image'


class SubEmotionInline(admin.TabularInline):
    model = SubEmotion
    extra = 0
    fields = ('name', 'image', 'tip', 'explanation')

    readonly_fields = ('image_preview',)

    def image_preview(self, instance):
        if instance.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', instance.image.url)
        return "-"

    image_preview.short_description = 'Image Preview'


class EmotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    inlines = [SubEmotionInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image'


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('lesson_number', 'text_explanation')


class ContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    inlines = [LessonInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image'


class LifeOverviewAdmin(admin.ModelAdmin):
    list_display = ('text_snippet', 'overview_preview',)

    def overview_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    overview_preview.short_description = 'Image Preview'

    def text_snippet(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_snippet.short_description = 'Text'


class NegativeThoughtsTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'explanation_snippet', 'tip_snippet')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 75px; height:auto;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'

    def explanation_snippet(self, obj):
        return obj.explanation[:50] + '...' if len(obj.explanation) > 50 else obj.explanation

    explanation_snippet.short_description = 'Explanation'

    def tip_snippet(self, obj):
        return obj.tip[:50] + '...' if len(obj.tip) > 50 else obj.tip

    tip_snippet.short_description = 'Tip'


class MeditationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 75px; height:auto;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


class TopicActivityInline(admin.TabularInline):
    model = TopicActivity
    extra = 0
    fields = ('order', 'tags', 'activity_text')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    inlines = [TopicActivityInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


@admin.register(DepressionTestQuestion)
class DepressionTestQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question_text',)


admin.site.register(Topic, TopicAdmin)

admin.site.register(NegativeThoughtsType, NegativeThoughtsTypeAdmin)
admin.site.register(Meditation, MeditationAdmin)
admin.site.register(LifeOverview, LifeOverviewAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Emotion, EmotionAdmin)
