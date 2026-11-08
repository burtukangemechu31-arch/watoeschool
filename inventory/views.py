# inventory/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SchoolAsset, AssetCategory

@login_required
def inventory_dashboard(request):
    assets = SchoolAsset.objects.all().order_by('-id')
    categories = AssetCategory.objects.all()
    
    query = request.GET.get('q', '')
    if query:
        assets = assets.filter(name__icontains=query) | assets.filter(serial_number__icontains=query) | assets.filter(location__icontains=query)

    return render(request, 'inventory/dashboard.html', {
        'assets': assets,
        'categories': categories,
        'query': query,
    })