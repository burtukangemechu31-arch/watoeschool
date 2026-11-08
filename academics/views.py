# academics/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Section, MarkAssessment, TimetableSlot

@login_required
def student_dashboard(request, student_id=None):
    """Renders the student dashboard or specific student profile view."""
    if student_id:
        student = get_object_or_404(StudentProfile, student_id=student_id)
    else:
        # Fallback to logged-in user's profile if available
        student = getattr(request.user, 'studentprofile', None)
    
    context = {'student': student}
    return render(request, 'academics/student_dashboard.html', context)

@login_required
def register_student(request):
    """Handles student registration form."""
    return render(request, 'academics/register_student.html')

@login_required
def timetable_index(request):
    """Renders the timetable index page."""
    slots = TimetableSlot.objects.all()
    return render(request, 'academics/timetable_index.html', {'slots': slots})

@login_required
def view_timetable(request, section_id):
    """Renders timetable for a specific section."""
    section = get_object_or_404(Section, id=section_id)
    slots = TimetableSlot.objects.filter(section=section)
    return render(request, 'academics/timetable.html', {'section': section, 'slots': slots})

@login_required
def student_report_card(request, student_id):
    """Renders the official student report card and promotion certificate."""
    student = get_object_or_404(StudentProfile, student_id=student_id)
    assessments = MarkAssessment.objects.filter(student=student)
    context = {'student': student, 'assessments': assessments}
    return render(request, 'academics/report_card.html', context)

@login_required
def download_report_card(request, student_id, semester):
    """Placeholder view for downloading report card PDF."""
    student = get_object_or_404(StudentProfile, student_id=student_id)
    return HttpResponse(f"Report card PDF for {student.student_id}, Semester {semester}")

@login_required
def admin_reports_dashboard(request):
    """Renders the admin academic reports overview dashboard."""
    return render(request, 'academics/admin_reports.html')

@login_required
def student_roster(request, section_id):
    """Renders the official Section Grade Roster (Mark List)."""
    section = get_object_or_404(Section, id=section_id)
    students = StudentProfile.objects.filter(section=section)
    context = {'section': section, 'students': students}
    return render(request, 'academics/roster.html', context)

@login_required
def student_transcript(request, student_id):
    """Renders the official 4-year longitudinal Academic Transcript (Grades 9-12)."""
    student = get_object_or_404(StudentProfile, student_id=student_id)
    assessments = MarkAssessment.objects.filter(student=student)
    context = {'student': student, 'assessments': assessments}
    return render(request, 'academics/transcript.html', context)

@login_required
def student_gate_id(request, student_id):
    """Renders a printable/scannable Student Gate ID badge."""
    student = get_object_or_404(StudentProfile, student_id=student_id)
    context = {'student': student}
    return render(request, 'academics/gate_id.html', context)

@login_required
def download_student_template(request):
    """Template download for bulk student uploads."""
    return HttpResponse("Student CSV Template")

@login_required
def bulk_upload_students(request):
    """Handles bulk student profile uploads."""
    return HttpResponse("Bulk upload processed successfully.")