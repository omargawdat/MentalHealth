from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import NegativeThinkingType, CBTQuestion


@admin.register(NegativeThinkingType)
class NegativeThinkingTypeAdmin(ModelAdmin):
    list_display = ['name', 'short_explanation', 'question_count']
    search_fields = ['name', 'explanation']
    list_filter = ['questions__is_general']

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Details'), {
            'fields': ('explanation', 'tips'),
            'classes': ('collapse',)
        }),
    )

    @display(description=_("Explanation"), ordering="explanation")
    def short_explanation(self, obj):
        return obj.explanation[:50] + '...' if len(obj.explanation) > 50 else obj.explanation

    @display(description=_("Questions"), ordering="questions_count")
    def question_count(self, obj):
        return obj.questions_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            questions_count=Count('questions')
        )


@admin.register(CBTQuestion)
class CBTQuestionAdmin(ModelAdmin):
    list_display = ['question_preview', 'thinking_type_info', 'is_general', 'has_tip']
    list_filter = ['is_general', 'thinking_type']
    search_fields = ['question_text', 'thinking_type__name']
    autocomplete_fields = ['thinking_type']

    fieldsets = (
        (None, {
            'fields': ('question_text', 'thinking_type', 'is_general')
        }),
        (_('Additional Information'), {
            'fields': ('after_question_tip',),
            'classes': ('collapse',)
        }),
    )

    @display(description=_("Question"), ordering="question_text")
    def question_preview(self, obj):
        return obj.question_text[:60] + '...' if len(obj.question_text) > 60 else obj.question_text

    @display(description=_("Thinking Type"), ordering="thinking_type__name")
    def thinking_type_info(self, obj):
        return obj.thinking_type.name if obj.thinking_type else _("Not Assigned")

    @display(description=_("Has Tip"), boolean=True)
    def has_tip(self, obj):
        return bool(obj.after_question_tip)
