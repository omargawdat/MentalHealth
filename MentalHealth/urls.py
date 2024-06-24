from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace='social')),

    path("admin/", admin.site.urls),
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.depression_test.urls")),
    path("api/", include("apps.journal.urls")),
    path("api/", include("apps.meditation.urls")),
    path("api/", include("apps.weekly.urls")),
    path("api/", include("apps.cbt.urls")),
    path("api/", include("apps.learning.urls")),
    path("api/", include("apps.plan.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
