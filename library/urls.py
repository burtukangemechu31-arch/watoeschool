# library/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_catalog, name='library_catalog'),
    path('download/<int:book_id>/', views.download_digital_book, name='download_digital_book'),
]