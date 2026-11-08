# exams/admin.py
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Exam, Question, ExamSubmission, MarkAssessment


class QuestionInline(TabularInline):
    model = Question
    extra = 1
    tab = True
    fields = [
        'text', 'question_image', 
        'option_a', 'option_a_image', 
        'option_b', 'option_b_image', 
        'option_c', 'option_c_image', 
        'option_d', 'option_d_image', 
        'correct_option', 'marks'
    ]


@admin.register(Exam)
class ExamAdmin(ModelAdmin):
    list_display = ['title', 'subject', 'show_grade_badge', 'duration_minutes', 'show_status_badge', 'bulk_actions_links', 'created_at']
    list_filter = ['grade_level', 'subject', 'is_active']
    search_fields = ['title', 'subject']
    inlines = [QuestionInline]

    @display(description="Grade Level", label=True)
    def show_grade_badge(self, obj):
        return f"Grade {obj.grade_level}"

    @display(description="Status", label={
        True: "success",
        False: "danger",
    })
    def show_status_badge(self, obj):
        return obj.is_active

    @display(description="Bulk CSV Actions")
    def bulk_actions_links(self, obj):
        return format_html(
            '<div style="display: flex; gap: 6px;">'
            '<a class="button" href="{}" style="background:#059669; color:white; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:600; text-decoration:none;">Questions CSV</a>'
            '<a class="button" href="{}" style="background:#4b5563; color:white; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:600; text-decoration:none;">Results CSV</a>'
            '</div>',
            f'/exams/questions/upload/{obj.id}/',
            '/exams/results/upload/'
        )


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ['exam', 'text_preview', 'show_correct_option', 'marks']
    list_filter = ['correct_option', 'exam__subject']
    search_fields = ['text']

    def text_preview(self, obj):
        return obj.text[:60] + "..." if len(obj.text) > 60 else obj.text
    text_preview.short_description = "Question Statement"

    @display(description="Correct Answer", label=True)
    def show_correct_option(self, obj):
        return f"Option {obj.correct_option}"


@admin.register(ExamSubmission)
class ExamSubmissionAdmin(ModelAdmin):
    list_display = ['student', 'exam', 'score_obtained', 'show_completion_badge', 'submitted_at']
    list_filter = ['is_completed', 'exam']
    search_fields = ['student__user__username', 'exam__title']

    @display(description="Submission Status", label={
        True: "info",
        False: "warning",
    })
    def show_completion_badge(self, obj):
        return "Completed" if obj.is_completed else "In Progress"


@admin.register(MarkAssessment)
class MarkAssessmentAdmin(ModelAdmin):
    list_display = ['student', 'subject', 'score', 'max_score']
    list_filter = ['subject']
    search_fields = ['student__user__username', 'subject']