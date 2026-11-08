# attendance/models.py
from django.db import models
from django.utils import timezone
from academics.models import StudentProfile, Section

class DailyAttendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"

class GateLog(models.Model):
    DIRECTION_CHOICES = [
        ('IN', 'Check-In'),
        ('OUT', 'Check-Out'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, default='IN')
    guard_notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.student} {self.direction} at {self.timestamp.strftime('%H:%M')}"