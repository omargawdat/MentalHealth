from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import Meditation


@admin.register(Meditation)
class MeditationAdmin(ModelAdmin):
    list_display = ['name', 'image_preview', 'url_link', 'duration_display']
    list_filter = ['duration']
    search_fields = ['name', 'url']
    readonly_fields = ['image_preview', 'url_link']
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'image_preview', 'url', 'url_link', 'duration')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = _("Image Preview")

    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)

    url_link.short_description = _("URL")

    def duration_display(self, obj):
        if obj.duration:
            minutes, seconds = divmod(obj.duration.total_seconds(), 60)
            return f"{int(minutes)}:{int(seconds):02d}"
        return "N/A"

    duration_display.short_description = _("Duration")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
