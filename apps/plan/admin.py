from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Topic, Activity, UserActivity, Level, DepActivity, UserDepActivity


class ActivityInline(TabularInline):
    model = Activity
    extra = 1
    autocomplete_fields = ['tag']


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ['name', 'color_display', 'image_preview', 'activity_count']
    search_fields = ['name', 'description']
    inlines = [ActivityInline]

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px;">{}</span>',
            obj.color, obj.color
        )

    color_display.short_description = 'Color'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image'

    def activity_count(self, obj):
        return obj.activity_set.count()

    activity_count.short_description = 'Activities'


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ['text_preview', 'topic', 'tag']
    list_filter = ['topic', 'tag']
    search_fields = ['text', 'topic__name', 'tag__name']
    autocomplete_fields = ['topic', 'tag']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Text Preview'


class UserActivityInline(TabularInline):
    model = UserActivity
    extra = 0
    readonly_fields = ['updated_at']
    autocomplete_fields = ['topic', 'tag']


@admin.register(UserActivity)
class UserActivityAdmin(ModelAdmin):
    list_display = ['user', 'topic', 'tag', 'number', 'flag', 'updated_at']
    list_filter = ['flag', 'topic', 'tag']
    search_fields = ['user__username', 'topic__name', 'tag__name', 'text']
    autocomplete_fields = ['topic', 'tag']
    readonly_fields = ['updated_at']


class DepActivityInline(TabularInline):
    model = DepActivity
    extra = 1
    autocomplete_fields = ['tag']


@admin.register(Level)
class LevelAdmin(ModelAdmin):
    list_display = ['name', 'activity_count']
    search_fields = ['name']
    inlines = [DepActivityInline]

    def activity_count(self, obj):
        return obj.depactivity_set.count()

    activity_count.short_description = 'Activities'


@admin.register(DepActivity)
class DepActivityAdmin(ModelAdmin):
    list_display = ['text_preview', 'level', 'tag']
    list_filter = ['level', 'tag']
    search_fields = ['text', 'level__name', 'tag__name']
    autocomplete_fields = ['level', 'tag']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Text Preview'


class UserDepActivityInline(TabularInline):
    model = UserDepActivity
    extra = 0
    readonly_fields = ['updated_at']
    autocomplete_fields = ['level', 'tag']


@admin.register(UserDepActivity)
class UserDepActivityAdmin(ModelAdmin):
    list_display = ['user', 'level', 'tag', 'number', 'flag', 'updated_at']
    list_filter = ['flag', 'level', 'tag']
    search_fields = ['user__username', 'level__name', 'tag__name', 'text']
    autocomplete_fields = ['level', 'tag']
    readonly_fields = ['updated_at']
