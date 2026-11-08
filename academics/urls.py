# academics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Existing Academic Routes
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/<str:student_id>/', views.student_dashboard, name='student_dashboard_detail'),
    path('register/', views.register_student, name='register_student'),
    path('timetable/', views.timetable_index, name='timetable_index'),
    path('timetable/<int:section_id>/', views.view_timetable, name='view_timetable'),
    path('report-card/<str:student_id>/', views.student_report_card, name='student_report_card'),
    path('report-card/<str:student_id>/pdf/<int:semester>/', views.download_report_card, name='download_report_card'),
    path('reports/admin/', views.admin_reports_dashboard, name='admin_reports_dashboard'),

    # Official Academic Documents, Gate IDs & Printing Suites
    path('section/<int:section_id>/roster/', views.student_roster, name='student_roster'),
    path('student/<str:student_id>/transcript/', views.student_transcript, name='student_transcript'),
    path('student/<str:student_id>/gate-id/', views.student_gate_id, name='student_gate_id'),

    # Bulk Student Upload & Template Utilities
    path('students/template/', views.download_student_template, name='download_student_template'),
    path('students/upload/', views.bulk_upload_students, name='bulk_upload_students'),
]