# wordknox/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import custom admin views
from notifications import admin_views as notification_admin_views

# API version prefix
API_VERSION = 'v1'

urlpatterns = [
    # Custom Admin Reply View for Messages (MUST be before admin.site.urls)
    path('admin/notifications/message/<uuid:message_id>/reply/', 
         notification_admin_views.reply_to_message, 
         name='admin_reply_to_message'),
    path('admin/notifications/quick-reply/', 
         notification_admin_views.quick_reply_api, 
         name='admin_quick_reply'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # CKEditor 5 URLs for file uploads
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
    # API v1 Endpoints
    path(f'api/{API_VERSION}/accounts/', include('accounts.urls')),
    path(f'api/{API_VERSION}/accounts/', include('dj_rest_auth.urls')),
    path(f'api/{API_VERSION}/core/', include('core.urls')),
    path(f'api/{API_VERSION}/projects/', include('projects.urls')),
    path(f'api/{API_VERSION}/blog/', include('blog.urls')),
    path(f'api/{API_VERSION}/services/', include('services.urls')),
    path(f'api/{API_VERSION}/products/', include('products.urls')),
    path(f'api/{API_VERSION}/business/', include('business.urls')),
    path(f'api/{API_VERSION}/notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
