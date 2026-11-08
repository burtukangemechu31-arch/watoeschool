# communications/admin.py
from django.contrib import admin
from .models import SMSLog

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('recipient_student', 'parent_phone', 'message_type', 'status', 'sent_at')
    list_filter = ('message_type', 'status', 'sent_at')
    search_fields = ('recipient_student__student_id', 'parent_phone')