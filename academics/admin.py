# academics/admin.py
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import AcademicYear, Program, GradeLevel, Stream, Section, StudentProfile, Subject, MarkAssessment, Classroom, TimetableSlot

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'e.g., WATO-2026-001'}),
            'parent_phone': forms.TextInput(attrs={'placeholder': 'e.g., 0911234567'}),
        }

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    form = StudentProfileForm
    list_display = ('student_id', 'user', 'section', 'program', 'parent_phone', 'view_documents')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name')

    def view_documents(self, obj):
        return format_html(
            '<a class="button" href="/academics/report-card/{}/" target="_blank" style="background:#059669; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Card</a>&nbsp;'
            '<a class="button" href="/academics/student/{}/transcript/" target="_blank" style="background:#1e293b; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Transcript</a>&nbsp;'
            '<a class="button" href="/academics/student/{}/gate-id/" target="_blank" style="background:#d97706; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Gate ID</a>',
            obj.student_id, obj.student_id, obj.student_id
        )
    view_documents.short_description = "Printable Documents & IDs"

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'academic_year', 'view_roster')

    def view_roster(self, obj):
        return format_html(
            '<a class="button" href="/academics/section/{}/roster/" target="_blank" style="background:#059669; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Print Roster</a>',
            obj.id
        )
    view_roster.short_description = "Grade Roster"

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_current')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level')
    list_filter = ('grade_level',)

@admin.register(MarkAssessment)
class MarkAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester')
    list_filter = ('semester', 'subject')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('section', 'day', 'period_number', 'subject')
    list_filter = ('section', 'day')