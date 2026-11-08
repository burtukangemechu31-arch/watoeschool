# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.exams_dashboard, name='exams_dashboard'),
    path('take/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('result/<int:submission_id>/', views.exam_result, name='exam_result'),
    
    # Bulk Upload & Templates
    path('questions/template/', views.download_question_template, name='download_question_template'),
    path('questions/upload/<int:exam_id>/', views.bulk_upload_questions, name='bulk_upload_questions'),
    path('results/template/', views.download_result_template, name='download_result_template'),
    path('results/upload/', views.bulk_upload_results, name='bulk_upload_results'),
]