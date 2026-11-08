# communications/models.py
from django.db import models
from django.utils import timezone
from academics.models import StudentProfile

class SMSLog(models.Model):
    MESSAGE_TYPES = [
        ('Attendance', 'Attendance Alert'),
        ('Fee', 'Fee Reminder'),
        ('Exam', 'Exam Result Notice'),
        ('General', 'General Announcement'),
    ]

    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending'),
    ]

    recipient_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='sms_logs')
    parent_phone = models.CharField(max_length=20)
    message_type = models.CharField(max_length=30, choices=MESSAGE_TYPES, default='General')
    message_body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.message_type}] To {self.parent_phone} ({self.status}) - {self.sent_at.strftime('%Y-%m-%d')}"