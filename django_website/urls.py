from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include('users.urls')),
    path("", include('main.urls')),
    # path("", include('Attendance.urls')),
    # path("", include('FaceRegistration.urls')),
    path("", include('locations.urls')),

    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)