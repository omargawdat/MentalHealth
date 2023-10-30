from django.contrib import admin

from apps.depression_test.models import AnswerOption, TestQuestion


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'label', 'value', ]
    search_fields = ['label']
    list_editable = ['label']


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']
    search_fields = ['question']

# @admin.register(DepressionAssessment)
# class DepressionAssessmentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'total_score', 'level_of_depression', 'date']
#     search_fields = ['user__username', 'level_of_depression']
#     list_filter = ['level_of_depression', 'date']
#     ordering = ['-date']
