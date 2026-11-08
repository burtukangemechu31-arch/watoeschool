# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'System Administrator'),
        ('registrar', 'Record Office'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('finance', 'Finance Officer'),
        ('librarian', 'Librarian'),
        ('guard', 'Security Guard'),
        ('inventory', 'Storekeeper'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"