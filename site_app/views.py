import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .content import BLOG_POSTS, PROCESS_STEPS, SERVICES
from .forms import ContactForm
from .models import BlogPost, Lead, PortfolioProject, Testimonial

logger = logging.getLogger(__name__)


def _footer_posts():
    return BlogPost.objects.filter(status=BlogPost.PUBLISHED)[:2]


def public_testimonials(limit=3):
    """Genuine, published testimonials only. Development samples appear only when DEBUG is on."""
    qs = Testimonial.objects.filter(is_published=True)
    if not settings.DEBUG:
        qs = qs.filter(is_sample=False)
    return qs[:limit]


def home(request):
    return render(request, "site_app/index.html", {
        "testimonials": public_testimonials(),
        "projects": PortfolioProject.objects.filter(is_published=True)[:4],
        "services": SERVICES,
        "process_steps": PROCESS_STEPS,
        "latest_articles": BlogPost.objects.filter(status=BlogPost.PUBLISHED).exclude(slug=None)[:3],
        "posts": _footer_posts(),
        "active": "home",
    })


def services(request):
    return render(request, "site_app/services.html", {
        "services": SERVICES, "posts": _footer_posts(), "active": "services",
    })


def portfolio(request):
    return render(request, "site_app/portfolio.html", {
        "projects": PortfolioProject.objects.filter(is_published=True),
        "posts": _footer_posts(), "active": "portfolio",
    })


def about(request):
    return render(request, "site_app/about.html", {"posts": _footer_posts(), "active": "about"})


def team(request):
    return render(request, "site_app/team.html", {"posts": _footer_posts(), "active": "team"})


def _notify(lead):
    """Email the team about a new lead. Records the real outcome; never raises."""
    if not settings.EMAIL_HOST_USER:
        return Lead.EMAIL_NOT_CONFIGURED
    try:
        send_mail(
            subject=f"New enquiry from {lead.name}",
            message=(f"Name: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\n"
                     f"Service: {lead.service}\n\n{lead.message}"),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.LEAD_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        return Lead.EMAIL_SENT
    except Exception:
        logger.exception("Lead %s saved but the notification email failed", lead.pk)
        return Lead.EMAIL_FAILED


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            lead = form.save()
            lead.email_status = _notify(lead)
            lead.save(update_fields=["email_status"])
            # The lead is saved either way, so this message is truthful regardless of email.
            messages.success(request, "Thanks, we've received your message and will reply to the email you gave us.")
            return redirect("contact")
    else:
        initial = {}
        wanted = request.GET.get("service", "")
        if wanted in dict(ContactForm.SERVICE_CHOICES):
            initial["service"] = wanted
        form = ContactForm(initial=initial)
    return render(request, "site_app/contact.html", {
        "form": form, "posts": _footer_posts(), "active": "contact",
    })


def blog(request):
    published = BlogPost.objects.filter(status=BlogPost.PUBLISHED)
    return render(request, "site_app/blog.html", {
        "articles": published.exclude(slug=None).exclude(title=""),
        "notes": published.filter(slug=None) | published.filter(title=""),
        "posts": published[:2], "active": "blog",
    })


def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.status != BlogPost.PUBLISHED and not (request.user.is_authenticated and request.user.is_staff):
        raise Http404
    related = BlogPost.objects.filter(status=BlogPost.PUBLISHED).exclude(slug=None).exclude(pk=post.pk)[:2]
    cta = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    return render(request, "site_app/blog_post.html", {
        "post": post, "related": related, "cta": cta,
        "posts": _footer_posts(), "active": "blog",
    })


def custom_404(request, exception):
    return render(request, "site_app/404.html", {}, status=404)
