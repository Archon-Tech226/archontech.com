from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve as media_serve
from site_app import admin_dashboard

urlpatterns = [
    path("admin/live-stats/", admin_dashboard.live_stats_view, name="admin_live_stats"),
    path("admin/live-stats/lead-status/", admin_dashboard.lead_status_view, name="admin_lead_status"),
    path("admin/live-stats/calendar/", admin_dashboard.calendar_month_view, name="admin_calendar"),
    path("admin/live-stats/day/", admin_dashboard.calendar_day_view, name="admin_calendar_day"),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("", include("site_app.urls")),
]

handler404 = "site_app.views.custom_404"

# Serve uploaded/seeded media in production too. Fine for a small brochure site; note that
# Render's free disk is ephemeral, so new uploads there are lost on redeploy (see README).
urlpatterns += [
    re_path(r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"), media_serve,
            {"document_root": settings.MEDIA_ROOT}),
]
