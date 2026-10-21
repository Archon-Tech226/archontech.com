from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from site_app import admin_dashboard

urlpatterns = [
    path("admin/live-stats/", admin_dashboard.live_stats_view, name="admin_live_stats"),
    path("admin/live-stats/lead-status/", admin_dashboard.lead_status_view, name="admin_lead_status"),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("", include("site_app.urls")),
]

handler404 = "site_app.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
