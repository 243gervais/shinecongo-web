"""
URL configuration for Shine Congo.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

# Customization de l'admin
admin.site.site_header = "Shine Congo Administration"
admin.site.site_title = "Shine Congo Admin"
admin.site.index_title = "Gérer votre site Shine Congo"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Favicon redirect (browsers often check /favicon.ico directly)
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')), name='favicon'),
    
    # Core pages
    path('', include('core.urls')),
    
    # Careers
    path('carrieres/', include('careers.urls')),
    
    # Applications
    path('', include('applications.urls')),
    
    # Contact
    path('contact/', include('contact.urls')),
    
    # Admin Panel
    path('admin-panel/', include('admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

