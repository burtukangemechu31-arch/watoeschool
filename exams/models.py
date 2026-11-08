# exams/models.py
from django.db import models

class Exam(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    grade_level = models.IntegerField(default=12)
    duration_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade {self.grade_level} {self.subject} - {self.title}"


class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="Supports text, LaTeX math (e.g., $x^2$), and chemical notation (e.g., $H_2SO_4$).")
    question_image = models.ImageField(upload_to='exam_questions/', blank=True, null=True, help_text="Optional diagram or formula image.")
    
    option_a = models.TextField(blank=True, default="", verbose_name="Option A Text")
    option_a_image = models.ImageField(upload_to='exam_options/', blank=True, null=True)
    
    option_b = models.TextField(blank=True, default="", verbose_name="Option B Text")
    option_b_image = models.ImageField(upload_to='exam_options/', blank=True, null=True)
    
    option_c = models.TextField(blank=True, default="", verbose_name="Option C Text")
    option_c_image = models.ImageField(upload_to='exam_options/', blank=True, null=True)
    
    option_d = models.TextField(blank=True, default="", verbose_name="Option D Text")
    option_d_image = models.ImageField(upload_to='exam_options/', blank=True, null=True)
    
    correct_option = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="Correct Answer")
    marks = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    def __str__(self):
        return f"Q: {self.text[:50]}... (Answer: {self.correct_option})"


class ExamSubmission(models.Model):
    student = models.ForeignKey('academics.StudentProfile', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    score_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now=True)


class MarkAssessment(models.Model):
    student = models.ForeignKey('academics.StudentProfile', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
