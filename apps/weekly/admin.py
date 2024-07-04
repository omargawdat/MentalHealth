from django.contrib import admin
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import LifeAspectType, LifeAspect, LifeActivity, LifeActivityTrack


class LifeActivityInline(TabularInline):
    model = LifeActivity
    extra = 1
    show_change_link = True


@admin.register(LifeAspectType)
class LifeAspectTypeAdmin(ModelAdmin):
    list_display = ['name', 'activity_count', 'average_aspect_value']
    search_fields = ['name']
    inlines = [LifeActivityInline]

    @display(description=_("Activities"), ordering="activity_count")
    def activity_count(self, obj):
        return obj.activities.count()

    @display(description=_("Avg. Aspect Value"), ordering="avg_value")
    def average_aspect_value(self, obj):
        avg = obj.lifeaspect_set.aggregate(Avg('value'))['value__avg']
        return f"{avg:.2f}" if avg else "N/A"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            activity_count=Count('activities', distinct=True),
            avg_value=Avg('lifeaspect__value')
        )


@admin.register(LifeAspect)
class LifeAspectAdmin(ModelAdmin):
    list_display = ['user', 'aspect_type', 'value', 'date']
    list_filter = ['aspect_type', 'date']
    search_fields = ['user__username', 'aspect_type__name']
    autocomplete_fields = ['aspect_type']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'aspect_type')


@admin.register(LifeActivity)
class LifeActivityAdmin(ModelAdmin):
    list_display = ['name', 'aspect_type', 'description_preview', 'tracked_count']
    list_filter = ['aspect_type']
    search_fields = ['name', 'description', 'aspect_type__name']
    autocomplete_fields = ['aspect_type']

    @display(description=_("Description Preview"))
    def description_preview(self, obj):
        return obj.description[:50] + '...' if obj.description and len(obj.description) > 50 else obj.description

    @display(description=_("Times Tracked"), ordering="tracked_count")
    def tracked_count(self, obj):
        return obj.tracked_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tracked_count=Count('activity_tracks', distinct=True)
        ).select_related('aspect_type')


class LifeActivityTrackInline(TabularInline):
    model = LifeActivityTrack
    extra = 1
    show_change_link = True
    readonly_fields = ['created_at']
    autocomplete_fields = ['life_activity']


@admin.register(LifeActivityTrack)
class LifeActivityTrackAdmin(ModelAdmin):
    list_display = ['user', 'life_activity', 'created_at', 'is_checked']
    list_filter = ['is_checked', 'created_at', 'life_activity__aspect_type']
    search_fields = ['user__username', 'life_activity__name']
    autocomplete_fields = ['life_activity', ]
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'life_activity', 'life_activity__aspect_type')
