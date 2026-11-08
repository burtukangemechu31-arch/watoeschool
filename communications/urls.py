# communications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.communications_dashboard, name='communications_dashboard'),
]