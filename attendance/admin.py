# attendance/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import DailyAttendance, GateLog

@admin.register(DailyAttendance)
class DailyAttendanceAdmin(ModelAdmin):
    list_display = ['student', 'section', 'date', 'show_status_badge', 'remarks']
    list_filter = ['status', 'date', 'section']
    search_fields = ['student__user__username', 'remarks']

    @display(description="Status", label={
        'Present': 'success',
        'Absent': 'danger',
        'Late': 'warning',
        'Excused': 'info',
    })
    def show_status_badge(self, obj):
        return obj.status

@admin.register(GateLog)
class GateLogAdmin(ModelAdmin):
    list_display = ['student', 'direction', 'timestamp', 'guard_notes']
    list_filter = ['direction', 'timestamp']
    search_fields = ['student__user__username', 'guard_notes']