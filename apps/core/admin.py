# admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import *


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)

    image_tag.short_description = 'Image'


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)

    image_tag.short_description = 'Image'


class SubEmotionInline(admin.StackedInline):  # Changed to StackedInline for better readability
    model = SubEmotion
    extra = 1  # Number of empty forms to display
    fields = ('name', 'image', 'tip', 'explanation')


class EmotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ['name']
    inlines = [SubEmotionInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Image'


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Emotion, EmotionAdmin)
