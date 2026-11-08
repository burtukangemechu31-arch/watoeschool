# wato_ims/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from academics.models import StudentProfile, Section
from inventory.models import SchoolAsset
from library.models import Book
from finance.models import FeePayment

User = get_user_model()

@login_required
def central_dashboard(request):
    """
    Renders the unified Wato IMS central dashboard with live system metrics 
    for authenticated staff and users.
    """
    total_students = StudentProfile.objects.count()
    total_teachers = User.objects.filter(is_staff=True).count()
    total_sections = Section.objects.count()
    total_assets = SchoolAsset.objects.count()
    total_books = Book.objects.count()
    
    payments = FeePayment.objects.all()
    total_revenue = sum(p.amount_paid for p in payments)

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_sections': total_sections,
        'total_assets': total_assets,
        'total_books': total_books,
        'total_revenue': total_revenue,
    }
    return render(request, 'dashboard.html', context)