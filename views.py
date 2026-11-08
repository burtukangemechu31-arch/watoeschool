# wato_ims/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def central_dashboard(request):
    """
    Renders the unified Wato IMS central dashboard for authenticated staff and users.
    """
    return render(request, 'dashboard.html')
