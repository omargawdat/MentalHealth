from django.contrib import admin

from apps.authentication.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'gender', 'date_joined', 'is_staff')
    list_filter = ('gender', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined',)
