# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('index/', views.attendance_index, name='attendance_index'),
    path('section/<int:section_id>/', views.section_attendance, name='section_attendance'),
]