# finance/admin.py
from django.contrib import admin
from django.utils.html import format_html
from finance.models import FeeCategory, StudentFee, FeePayment

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'academic_year')
    search_fields = ('name', 'academic_year')
    list_filter = ('academic_year',)

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_category', 'is_paid', 'assigned_date')
    list_filter = ('is_paid', 'fee_category', 'assigned_date')
    search_fields = ('student__student_id', 'student__user__first_name', 'student__user__last_name')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'student', 'fee_category', 'amount_paid', 'payment_date', 'recorded_by', 'view_receipt')
    search_fields = ('receipt_number', 'student__student_id', 'student__user__first_name', 'student__user__last_name')
    list_filter = ('payment_date', 'fee_category')

    def view_receipt(self, obj):
        return format_html(
            '<a class="button" href="/finance/receipt/{}/" target="_blank" style="background:#059669; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Print Receipt</a>',
            obj.id
        )
    view_receipt.short_description = "Official Receipt"