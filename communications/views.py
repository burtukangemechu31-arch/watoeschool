# communications/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SMSLog
from academics.models import StudentProfile

@login_required
def communications_dashboard(request):
    """
    Displays recent SMS logs and allows sending mock broadcast messages.
    """
    if request.method == 'POST':
        message_type = request.POST.get('message_type')
        message_body = request.POST.get('message_body')
        
        # Broadcast to all students with active profiles
        students = StudentProfile.objects.all()
        for student in students:
            phone = getattr(student, 'parent_phone', '0900000000') # fallback
            SMSLog.objects.create(
                recipient_student=student,
                parent_phone=phone,
                message_type=message_type,
                message_body=message_body,
                status='Sent'
            )
        return redirect('communications_dashboard')

    logs = SMSLog.objects.all().order_by('-sent_at')[:50]
    return render(request, 'communications/dashboard.html', {'logs': logs})