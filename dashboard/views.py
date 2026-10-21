from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from site_app.models import BlogPost, Testimonial, PortfolioProject, Lead
from .forms import BlogPostForm, TestimonialForm, PortfolioProjectForm, LeadStatusForm

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url="dashboard:login")


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/dashboard/"


class DashboardLogoutView(LogoutView):
    next_page = "dashboard:login"


@login_required(login_url="dashboard:login")
@staff_required
def home(request):
    week_ago = timezone.now() - timedelta(days=7)
    context = {
        "lead_count": Lead.objects.count(),
        "new_lead_count": Lead.objects.filter(status=Lead.NEW).count(),
        "lead_count_week": Lead.objects.filter(created_at__gte=week_ago).count(),
        "post_count": BlogPost.objects.filter(status=BlogPost.PUBLISHED).count(),
        "draft_count": BlogPost.objects.filter(status=BlogPost.DRAFT).count(),
        "testimonial_count": Testimonial.objects.filter(is_published=True, is_sample=False).count(),
        "sample_testimonial_count": Testimonial.objects.filter(is_sample=True).count(),
        "followups_due": Lead.objects.filter(follow_up_date__lte=timezone.localdate()).exclude(status__in=[Lead.WON, Lead.LOST]).count(),
        "project_count": PortfolioProject.objects.filter(is_published=True).count(),
        "recent_leads": Lead.objects.all()[:5],
        "recent_posts": BlogPost.objects.all()[:5],
    }
    return render(request, "dashboard/home.html", context)


# --- Leads -------------------------------------------------------------
@login_required(login_url="dashboard:login")
@staff_required
def leads_list(request):
    qs = Lead.objects.all()
    status = request.GET.get("status", "")
    q = request.GET.get("q", "")
    if status:
        qs = qs.filter(status=status)
    if request.GET.get("followup"):
        qs = qs.filter(follow_up_date__lte=timezone.localdate()).exclude(status__in=[Lead.WON, Lead.LOST])
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(message__icontains=q))
    return render(request, "dashboard/leads_list.html", {
        "leads": qs, "status": status, "q": q, "status_choices": Lead.STATUS_CHOICES,
    })


@login_required(login_url="dashboard:login")
@staff_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        form = LeadStatusForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request"):
                return render(request, "dashboard/_lead_status_panel.html", {"lead": lead, "form": form, "saved": True})
            messages.success(request, "Lead updated.")
            return redirect("dashboard:lead_detail", pk=pk)
    else:
        form = LeadStatusForm(instance=lead)
    return render(request, "dashboard/lead_detail.html", {"lead": lead, "form": form})


# --- Blog posts ----------------------------------------------------------
@login_required(login_url="dashboard:login")
@staff_required
def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, "dashboard/blog_list.html", {"posts": posts})


@login_required(login_url="dashboard:login")
@staff_required
def blog_form(request, pk=None):
    post = get_object_or_404(BlogPost, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.title and obj.status == BlogPost.PUBLISHED and not obj.excerpt:
                obj.excerpt = obj.body[:200]
            if not obj.author_id:
                obj.author = request.user
            obj.save()
            messages.success(request, "Post saved.")
            return redirect("dashboard:blog_list")
    else:
        form = BlogPostForm(instance=post)
    return render(request, "dashboard/blog_form.html", {"form": form, "post": post})


@login_required(login_url="dashboard:login")
@staff_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("dashboard:blog_list")


# --- Testimonials ----------------------------------------------------------
@login_required(login_url="dashboard:login")
@staff_required
def testimonial_list(request):
    items = Testimonial.objects.all()
    return render(request, "dashboard/testimonial_list.html", {"items": items})


@login_required(login_url="dashboard:login")
@staff_required
def testimonial_form(request, pk=None):
    item = get_object_or_404(Testimonial, pk=pk) if pk else None
    if request.method == "POST":
        form = TestimonialForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial saved.")
            return redirect("dashboard:testimonial_list")
    else:
        form = TestimonialForm(instance=item)
    return render(request, "dashboard/testimonial_form.html", {"form": form, "item": item})


@login_required(login_url="dashboard:login")
@staff_required
def testimonial_delete(request, pk):
    item = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Testimonial deleted.")
    return redirect("dashboard:testimonial_list")


# --- Portfolio ----------------------------------------------------------
@login_required(login_url="dashboard:login")
@staff_required
def portfolio_list(request):
    items = PortfolioProject.objects.all()
    return render(request, "dashboard/portfolio_list.html", {"items": items})


@login_required(login_url="dashboard:login")
@staff_required
def portfolio_form(request, pk=None):
    item = get_object_or_404(PortfolioProject, pk=pk) if pk else None
    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Project saved.")
            return redirect("dashboard:portfolio_list")
    else:
        form = PortfolioProjectForm(instance=item)
    return render(request, "dashboard/portfolio_form.html", {"form": form, "item": item})


@login_required(login_url="dashboard:login")
@staff_required
def portfolio_delete(request, pk):
    item = get_object_or_404(PortfolioProject, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Project deleted.")
    return redirect("dashboard:portfolio_list")
