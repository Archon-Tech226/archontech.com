"""JSON endpoints behind the live admin home dashboard (staff only)."""
import json
from datetime import timedelta

from django.contrib import admin
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import BlogPost, Lead, PortfolioProject, Testimonial


@require_GET
def live_stats(request):
    try:
        days = int(request.GET.get("days", 14))
    except ValueError:
        days = 14
    days = days if days in (7, 14, 30) else 14

    now = timezone.now()
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    counts = {}
    for dt in Lead.objects.filter(created_at__date__gte=start).values_list("created_at", flat=True):
        d = timezone.localtime(dt).date()
        counts[d] = counts.get(d, 0) + 1
    series = []
    for i in range(days):
        d = start + timedelta(days=i)
        series.append({"label": d.strftime("%d %b"), "count": counts.get(d, 0)})

    status_counts = {code: Lead.objects.filter(status=code).count() for code, _ in Lead.STATUS_CHOICES}
    recent = [{
        "id": l.pk, "name": l.name, "email": l.email, "service": l.service or "",
        "status": l.status, "created": timezone.localtime(l.created_at).strftime("%d %b, %I:%M %p"),
        "url": reverse("admin:site_app_lead_change", args=[l.pk]),
    } for l in Lead.objects.all()[:8]]

    return JsonResponse({
        "server_time": timezone.localtime(now).strftime("%I:%M:%S %p"),
        "days": days,
        "cards": {
            "leads_total": Lead.objects.count(),
            "leads_new": status_counts.get(Lead.NEW, 0),
            "leads_today": Lead.objects.filter(created_at__date=today).count(),
            "leads_week": Lead.objects.filter(created_at__gte=now - timedelta(days=7)).count(),
            "followups_due": Lead.objects.filter(follow_up_date__lte=today).exclude(
                status__in=[Lead.WON, Lead.LOST]).count(),
            "posts_published": BlogPost.objects.filter(status=BlogPost.PUBLISHED).count(),
            "posts_draft": BlogPost.objects.filter(status=BlogPost.DRAFT).count(),
            "projects": PortfolioProject.objects.filter(is_published=True).count(),
            "testimonials": Testimonial.objects.filter(is_published=True, is_sample=False).count(),
        },
        "series": series,
        "status_counts": status_counts,
        "status_labels": dict(Lead.STATUS_CHOICES),
        "recent": recent,
    })


@require_POST
def lead_set_status(request):
    try:
        payload = json.loads(request.body or "{}")
        lead = Lead.objects.get(pk=int(payload["id"]))
    except (ValueError, KeyError, Lead.DoesNotExist):
        return JsonResponse({"ok": False, "error": "Lead not found"}, status=400)
    status = payload.get("status")
    if status not in dict(Lead.STATUS_CHOICES):
        return JsonResponse({"ok": False, "error": "Invalid status"}, status=400)
    lead.status = status
    lead.save(update_fields=["status"])
    return JsonResponse({"ok": True, "id": lead.pk, "status": status, "label": lead.get_status_display()})


# Wrapped so only logged-in staff can reach them (same rule as the admin itself).
live_stats_view = admin.site.admin_view(live_stats)
lead_status_view = admin.site.admin_view(lead_set_status)


# ---- Calendar -----------------------------------------------------------
import calendar as _cal
from datetime import date as _date


def _parse_month(value):
    try:
        y, m = value.split("-")
        y, m = int(y), int(m)
        if 1 <= m <= 12 and 2000 <= y <= 2100:
            return y, m
    except (ValueError, AttributeError):
        pass
    today = timezone.localdate()
    return today.year, today.month


@require_GET
def calendar_month(request):
    y, m = _parse_month(request.GET.get("month", ""))
    days_in_month = _cal.monthrange(y, m)[1]
    first_weekday = _date(y, m, 1).weekday()  # Monday = 0
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(timezone.datetime(y, m, 1), tz)
    end = timezone.make_aware(timezone.datetime(y + (m == 12), (m % 12) + 1, 1), tz)
    days = {}
    for dt in Lead.objects.filter(created_at__gte=start, created_at__lt=end).values_list("created_at", flat=True):
        d = timezone.localtime(dt).day
        days.setdefault(str(d), {"leads": 0, "followups": 0})["leads"] += 1
    for fd in Lead.objects.filter(follow_up_date__year=y, follow_up_date__month=m).exclude(
            status__in=[Lead.WON, Lead.LOST]).values_list("follow_up_date", flat=True):
        days.setdefault(str(fd.day), {"leads": 0, "followups": 0})["followups"] += 1
    today = timezone.localdate()
    return JsonResponse({
        "year": y, "month": m, "label": _date(y, m, 1).strftime("%B %Y"),
        "days_in_month": days_in_month, "first_weekday": first_weekday, "days": days,
        "today": today.day if (today.year, today.month) == (y, m) else None,
    })


@require_GET
def calendar_day(request):
    try:
        d = _date.fromisoformat(request.GET.get("date", ""))
    except ValueError:
        return JsonResponse({"error": "Invalid date"}, status=400)

    def row(l, kind):
        return {"id": l.pk, "name": l.name, "email": l.email, "service": l.service or "", "status": l.status,
                "time": timezone.localtime(l.created_at).strftime("%I:%M %p"), "kind": kind,
                "url": reverse("admin:site_app_lead_change", args=[l.pk])}

    created = [row(l, "enquiry") for l in Lead.objects.filter(created_at__date=d)]
    due = [row(l, "follow-up") for l in Lead.objects.filter(follow_up_date=d).exclude(
        status__in=[Lead.WON, Lead.LOST])]
    return JsonResponse({
        "date": d.isoformat(), "label": d.strftime("%A, %d %B %Y"), "items": created + due,
        "list_url": reverse("admin:site_app_lead_changelist") + f"?created_at__year={d.year}&created_at__month={d.month}&created_at__day={d.day}",
    })


calendar_month_view = admin.site.admin_view(calendar_month)
calendar_day_view = admin.site.admin_view(calendar_day)
