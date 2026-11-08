# attendance/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DailyAttendance, GateLog
from academics.models import Section

@login_required
def attendance_dashboard(request):
    """Displays student attendance history and gate security logs."""
    attendance_records = DailyAttendance.objects.all().order_by('-date')
    gate_logs = GateLog.objects.all().order_by('-timestamp')[:50]

    if hasattr(request.user, 'studentprofile'):
        attendance_records = attendance_records.filter(student=request.user.studentprofile)
        gate_logs = gate_logs.filter(student=request.user.studentprofile)

    return render(request, 'attendance/dashboard.html', {
        'attendance_records': attendance_records,
        'gate_logs': gate_logs
    })

@login_required
def attendance_index(request):
    """Index view for attendance management."""
    sections = Section.objects.all()
    return render(request, 'attendance/index.html', {'sections': sections})

@login_required
def section_attendance(request, section_id):
    """View and manage attendance for a specific section."""
    section = get_object_or_404(Section, id=section_id)
    records = DailyAttendance.objects.filter(section=section)
    return render(request, 'attendance/section_attendance.html', {
        'section': section,
        'records': records
    })