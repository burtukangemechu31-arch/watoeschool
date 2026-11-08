# finance/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FeePayment, StudentFee, FeeCategory
from django.db.models import Sum

@login_required
def finance_dashboard(request):
    """Renders the main finance overview dashboard for the school administration."""
    total_payments = FeePayment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
    recent_payments = FeePayment.objects.select_related('student', 'fee_category').order_by('-payment_date')[:10]
    pending_fees = StudentFee.objects.filter(is_paid=False).count()
    
    context = {
        'total_payments': total_payments,
        'recent_payments': recent_payments,
        'pending_fees': pending_fees,
    }
    return render(request, 'finance/dashboard.html', context)

@login_required
def payment_receipt(request, payment_id):
    """Renders an official printable fee payment receipt by primary key ID."""
    payment = get_object_or_404(FeePayment, id=payment_id)
    context = {'payment': payment}
    return render(request, 'finance/receipt.html', context)