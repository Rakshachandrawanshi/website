from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns
urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Main App (Dashboard, Profile, About, etc.)
    path('', include('main.urls')),
]

# Media files (Images, Uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)