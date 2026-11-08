# library/models.py
from django.db import models
from django.utils import timezone
from academics.models import StudentProfile

class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50, blank=True, null=True, verbose_name="ISBN Code")
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    shelf_location = models.CharField(max_length=50, blank=True, null=True)
    digital_file = models.FileField(upload_to='library/digital_books/', blank=True, null=True, verbose_name="Digital PDF Copy")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookBorrowing(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} borrowed {self.book.title}"