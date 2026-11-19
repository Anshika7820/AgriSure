from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("farms/", include("farms.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("negotiations/", include("negotiations.urls")),
    path("contracts/", include("contracts.urls")),
    path("deliveries/", include("deliveries.urls")),
    path("payments/", include("payments.urls")),
    path("notifications/", include("notifications.urls")),
    path("disputes/", include("disputes.urls")),
    path("reviews/", include("reviews.urls")),
    path("reports/", include("reports.urls")),
    path("", include("audit.urls")),
]

from django.views.static import serve
from django.urls import re_path

# Serve media files in both development and production
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
