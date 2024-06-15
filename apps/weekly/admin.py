from django.contrib import admin

from .models import LifeAspectType, LifeAspect


@admin.register(LifeAspectType)
class LifeAspectTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(LifeAspect)
class LifeAspectAdmin(admin.ModelAdmin):
    list_display = ('id', 'aspect_type', 'value')
    search_fields = ('aspect_type__name',)
    list_filter = ('aspect_type',)
