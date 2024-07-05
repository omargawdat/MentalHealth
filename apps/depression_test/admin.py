from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import AnswerOption, TestQuestion, DepressionTestAttempt


class AnswerOptionInline(TabularInline):
    model = TestQuestion.answer_options.through
    extra = 1
    verbose_name = _("Answer Option")
    verbose_name_plural = _("Answer Options")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AnswerOption)
class AnswerOptionAdmin(ModelAdmin):
    list_display = ['label', 'value']
    list_filter = ['value']
    search_fields = ['label']
    ordering = ['value']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            question_count=Count('testquestion', distinct=True)
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TestQuestion)
class TestQuestionAdmin(ModelAdmin):
    list_display = ['question', 'answer_options_display']
    search_fields = ['question']
    filter_horizontal = ['answer_options']
    inlines = [AnswerOptionInline]

    @display(description=_("Answer Options"))
    def answer_options_display(self, obj):
        return ", ".join([str(option) for option in obj.answer_options.all()])

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DepressionTestAttempt)
class DepressionTestAttemptAdmin(ModelAdmin):
    list_display = ['user_display', 'total_score', 'level_of_depression', 'timestamp']
    list_filter = ['level_of_depression', 'timestamp']
    search_fields = ['user__email', 'user__username']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']

    fieldsets = (
        (None, {
            'fields': ('user', 'total_score', 'level_of_depression')
        }),
        (_('Timestamp'), {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )

    @display(description=_("User"), ordering="user__email")
    def user_display(self, obj):
        return f"{obj.user.email} ({obj.user.username})"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
