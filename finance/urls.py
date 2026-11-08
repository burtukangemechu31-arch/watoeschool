# finance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
]