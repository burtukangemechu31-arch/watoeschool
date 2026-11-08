# guard/admin.py
from django.contrib import admin
from .models import GatePass

@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = ('student', 'approved_by', 'exit_time', 'expected_return_time', 'is_returned')
    list_filter = ('is_returned', 'exit_time')
    search_fields = ('student__student_id', 'approved_by', 'reason')