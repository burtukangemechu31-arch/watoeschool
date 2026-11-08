# guard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GatePass

@login_required
def guard_dashboard(request):
    query = request.GET.get('q', '')
    passes = GatePass.objects.all().order_by('-exit_time')
    
    if query:
        passes = passes.filter(student__student_id__icontains=query)

    return render(request, 'guard/dashboard.html', {'passes': passes, 'query': query})

@login_required
def mark_returned(request, pass_id):
    gate_pass = get_object_or_404(GatePass, id=pass_id)
    gate_pass.is_returned = True
    gate_pass.save()
    return redirect('guard_dashboard')