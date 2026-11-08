# guard/models.py
from django.db import models
from academics.models import StudentProfile

class GatePass(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.TextField(help_text="Reason for leaving school premises")
    exit_time = models.DateTimeField(auto_now_add=True)
    expected_return_time = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, help_text="Admin or Unit Leader name")
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Gate Pass for {self.student.student_id} - {self.exit_time.strftime('%Y-%m-%d %H:%M')}"