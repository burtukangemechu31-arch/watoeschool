# wato_ims/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import central_dashboard

urlpatterns = [
    # Central Portal Dashboard for Wato IMS
    path('', central_dashboard, name='central_dashboard'),
    
    # Unified Administration Panel
    path('admin/', admin.site.urls),
    
    # Modular App Routing (Including Accounts for Student/Staff Authentication)
    path('accounts/', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('exams/', include('exams.urls')),
    path('finance/', include('finance.urls')),
    path('library/', include('library.urls')),
    path('guard/', include('guard.urls')),
    path('inventory/', include('inventory.urls')),
    path('attendance/', include('attendance.urls')),
    path('communications/', include('communications.urls')),
]

# Serve media files (student photos, question diagrams, e-book PDFs) during local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)