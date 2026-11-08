# inventory/models.py
from django.db import models

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SchoolAsset(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Damaged', 'Damaged'),
        ('Maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    location = models.CharField(max_length=150, help_text="e.g., IT Lab 1, Physics Laboratory, Finance Office")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Good')
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.location})"