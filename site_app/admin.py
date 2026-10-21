from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Testimonial, PortfolioProject, Lead

admin.site.site_header = "Archon Tech Admin"
admin.site.site_title = "Archon Tech Admin"
admin.site.index_title = "Dashboard"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("__str__", "author_name", "category", "status", "created_at")
    list_filter = ("status", "category", "author_name")
    search_fields = ("title", "author_name", "body")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    fields = ("author", "author_name", "title", "slug", "category", "excerpt", "body", "status", "created_at", "updated_at")

    def short_body(self, obj):
        return (obj.body[:70] + "\u2026") if len(obj.body) > 70 else obj.body
    short_body.short_description = "Post"

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.author_name:
            obj.author_name = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "company", "stars", "is_published", "is_sample", "created_at")
    list_filter = ("is_published", "is_sample", "rating")
    search_fields = ("client_name", "company", "quote")
    list_editable = ("is_published",)

    def stars(self, obj):
        return "\u2605" * obj.rating + "\u2606" * (5 - obj.rating)
    stars.short_description = "Rating"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_type", "category", "is_published", "sort_order", "has_link")
    list_filter = ("project_type", "category", "is_published")
    search_fields = ("title", "description", "tech_tags")
    list_editable = ("sort_order", "is_published")

    def has_link(self, obj):
        return bool(obj.live_url)
    has_link.boolean = True
    has_link.short_description = "Live?"


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "status_badge", "email_status", "follow_up_date", "created_at")
    list_filter = ("status", "service", "email_status")
    search_fields = ("name", "email", "phone", "message")
    list_editable = ()
    readonly_fields = ("name", "email", "phone", "service", "message", "email_status", "created_at")
    fields = ("name", "email", "phone", "service", "message", "status", "follow_up_date", "notes", "email_status", "created_at")

    STATUS_COLORS = {
        "new": "#6425e8",
        "contacted": "#2563eb",
        "quoted": "#9fd81c",
        "won": "#16a34a",
        "lost": "#dc2626",
    }

    def status_badge(self, obj):
        color = self.STATUS_COLORS.get(obj.status, "#888")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600">{}</span>',
            color, obj.get_status_display(),
        )
    status_badge.short_description = "Status"
