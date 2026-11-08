# finance/models.py
from django.db import models
from django.utils import timezone
from academics.models import StudentProfile

class FeeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    academic_year = models.CharField(max_length=20, default="2019 E.C.")

    def __str__(self):
        return f"{self.name} - {self.amount} ETB"

class StudentFee(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    assigned_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.fee_category.name} ({'Paid' if self.is_paid else 'Pending'})"

class FeePayment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    receipt_number = models.CharField(max_length=50, unique=True)
    recorded_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number} - {self.student} ({self.amount_paid} ETB)"