# academics/models.py
from django.db import models
from accounts.models import User

class AcademicYear(models.Model):
    name = models.CharField(max_length=20, help_text="e.g., 2019 E.C.")
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    # Regular (2 Semesters) vs Night (3 Semesters)
    PROGRAM_TYPES = (
        ('regular', 'Regular (2 Semesters)'),
        ('night', 'Night (3 Semesters)'),
    )
    name = models.CharField(max_length=20, choices=PROGRAM_TYPES, unique=True)
    num_semesters = models.IntegerField(default=2)

    def __str__(self):
        return self.get_name_display()

class GradeLevel(models.Model):
    name = models.CharField(max_length=10, unique=True) # Grade 9, 10, 11, 12

    def __str__(self):
        return self.name

class Stream(models.Model):
    # For Grade 11 & 12 Natural / Social streams
    name = models.CharField(max_length=30, choices=(
        ('general', 'General (Grades 9-10)'),
        ('natural', 'Natural Science'),
        ('social', 'Social Science')
    ))

    def __str__(self):
        return self.get_name_display()

class Section(models.Model):
    name = models.CharField(max_length=20) # e.g., 11 Natural A
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.grade_level.name} - {self.name} ({self.program.name})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=30, unique=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class Subject(models.Model):
    name = models.CharField(max_length=50)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Grade {self.grade_level.name})"

class MarkAssessment(models.Model):
    # Added unique related_name to prevent reverse accessor name clashes
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_mark_assessments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField(help_text="1, 2, or 3")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    # Continuous assessment total out of 100
    total_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ('student', 'subject', 'semester', 'academic_year')

class Classroom(models.Model):
    name = models.CharField(max_length=20) # e.g., Room 204, Lab 1
    capacity = models.IntegerField(default=40)

class TimetableSlot(models.Model):
    DAYS_OF_WEEK = (
        ('1_Mon', 'Monday'),
        ('2_Tue', 'Tuesday'),
        ('3_Wed', 'Wednesday'),
        ('4_Thu', 'Thursday'),
        ('5_Fri', 'Friday'),
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    period_number = models.IntegerField(help_text="Period 1 to 8")
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('section', 'day', 'period_number') # Prevents double-booking a section