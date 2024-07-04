from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import (
    Emotion, JournalEntry,
    Activity, Reason, Tag, Preference, Tips, TipsStress
)


@admin.register(Emotion)
class EmotionAdmin(ModelAdmin):
    list_display = ['name', 'type', 'has_image']
    list_filter = ['type']
    search_fields = ['name', 'description']

    @display(boolean=True, description=_("Has Image"))
    def has_image(self, obj):
        return bool(obj.image)


@admin.register(JournalEntry)
class JournalEntryAdmin(ModelAdmin):
    list_display = ['user', 'date', 'has_stress', 'has_depression']
    list_filter = ['date', 'has_stress', 'has_depression']
    search_fields = ['user__email', 'notes']
    date_hierarchy = 'date'


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ['activity_text', 'has_image']
    search_fields = ['activity_text']

    @display(boolean=True, description=_("Has Image"))
    def has_image(self, obj):
        return bool(obj.activity_image)


@admin.register(Reason)
class ReasonAdmin(ModelAdmin):
    list_display = ['reason_text', 'has_image']
    search_fields = ['reason_text']

    @display(boolean=True, description=_("Has Image"))
    def has_image(self, obj):
        return bool(obj.reason_image)


class PreferenceInline(admin.TabularInline):
    model = Preference
    extra = 1


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'preference_count', 'tips_count']
    search_fields = ['name']
    inlines = [PreferenceInline]

    @display(description=_("Preferences"), ordering="preference_count")
    def preference_count(self, obj):
        return obj.preference_count

    @display(description=_("Tips"), ordering="tips_count")
    def tips_count(self, obj):
        return obj.tips_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            preference_count=Count('preference', distinct=True),
            tips_count=Count('tips', distinct=True)
        )


@admin.register(Tips)
class TipsAdmin(ModelAdmin):
    list_display = ['short_description', 'tag', 'emotion']
    list_filter = ['tag', 'emotion']
    search_fields = ['description', 'emotion']

    @display(description=_("Description"))
    def short_description(self, obj):
        return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description


@admin.register(TipsStress)
class TipsStressAdmin(ModelAdmin):
    list_display = ['short_description']
    search_fields = ['description']

    @display(description=_("Description"))
    def short_description(self, obj):
        return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description
