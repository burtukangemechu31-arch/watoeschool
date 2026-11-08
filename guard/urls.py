# guard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.guard_dashboard, name='guard_dashboard'),
    path('mark-returned/<int:pass_id>/', views.mark_returned, name='mark_returned'),
]