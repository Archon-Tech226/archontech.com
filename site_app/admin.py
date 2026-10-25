from django import forms
from django.contrib import admin, messages
from django.db import models
from django.utils.html import format_html

from .models import BlogPost, Lead, PortfolioProject, Testimonial

admin.site.site_header = "Archon Tech Admin"
admin.site.site_title = "Archon Tech Admin"
admin.site.index_title = "Dashboard"
admin.site.site_url = "/"

BIG_TEXT = {models.TextField: {"widget": forms.Textarea(attrs={"rows": 16})}}


def pill(kind, label):
    return format_html('<span class="at-pill st-{}">{}</span>', kind, label)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("headline", "category", "author_name", "status_pill", "created_at")
    list_filter = ("status", "category", "author_name")
    search_fields = ("title", "author_name", "body", "excerpt")
    date_hierarchy = "created_at"
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "public_link")
    formfield_overrides = BIG_TEXT
    actions = ["publish_posts", "unpublish_posts"]
    fieldsets = (
        ("Article", {"fields": ("title", "slug", "category", "excerpt", "body"),
                     "description": 'Tip: start a line with "## " for a heading and "- " for a bullet. '
                                    "Leave the title empty for a short note."}),
        ("Publishing", {"fields": ("status", "author_name", "author", "public_link", "created_at", "updated_at")}),
    )

    @admin.display(description="Post", ordering="title")
    def headline(self, obj):
        return obj.title or (obj.body[:60] + ("…" if len(obj.body) > 60 else ""))

    @admin.display(description="Status", ordering="status")
    def status_pill(self, obj):
        return pill(obj.status, obj.get_status_display())

    @admin.display(description="Public page")
    def public_link(self, obj):
        if obj.pk and obj.is_article:
            return format_html('<a class="at-link" href="{}" target="_blank" rel="noopener">View on site &nearr;</a>',
                               obj.get_absolute_url())
        return "Shown after saving an article with a title."

    @admin.action(description="Publish selected posts")
    def publish_posts(self, request, qs):
        self.message_user(request, f"{qs.update(status=BlogPost.PUBLISHED)} post(s) published.", messages.SUCCESS)

    @admin.action(description="Move selected posts back to draft")
    def unpublish_posts(self, request, qs):
        self.message_user(request, f"{qs.update(status=BlogPost.DRAFT)} post(s) set to draft.", messages.SUCCESS)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.author_name:
            obj.author_name = request.user.get_full_name() or request.user.username
        if obj.title and not obj.excerpt:
            obj.excerpt = obj.body[:200]
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "company", "stars", "visibility", "created_at")
    list_filter = ("is_published", "is_sample", "rating")
    search_fields = ("client_name", "company", "quote")
    actions = ["publish_selected", "hide_selected"]
    fieldsets = (
        ("Client", {"fields": ("client_name", "company")}),
        ("Testimonial", {"fields": ("quote", "rating"),
                         "description": "Only add words from a real client who has approved them."}),
        ("Visibility", {"fields": ("is_published", "is_sample"),
                        "description": "Samples are placeholders for development. They are never shown on the live "
                                       "site. Untick “sample” only when replacing it with a genuine, approved quote."}),
    )

    @admin.display(description="Rating")
    def stars(self, obj):
        return "\u2605" * obj.rating + "\u2606" * (5 - obj.rating)

    @admin.display(description="On live site")
    def visibility(self, obj):
        if obj.is_sample:
            return pill("sample", "Sample, never public")
        return pill("published" if obj.is_published else "draft", "Visible" if obj.is_published else "Hidden")

    @admin.action(description="Show selected on the site (non-samples only)")
    def publish_selected(self, request, qs):
        n = qs.filter(is_sample=False).update(is_published=True)
        self.message_user(request, f"{n} testimonial(s) now visible. Samples are skipped.", messages.SUCCESS)

    @admin.action(description="Hide selected from the site")
    def hide_selected(self, request, qs):
        self.message_user(request, f"{qs.update(is_published=False)} testimonial(s) hidden.", messages.SUCCESS)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "project_type", "category", "visibility", "sort_order", "has_link")
    list_display_links = ("thumb", "title")
    list_editable = ("sort_order",)
    list_filter = ("project_type", "category", "is_published")
    search_fields = ("title", "description", "tech_tags")
    readonly_fields = ("image_preview", "created_at")
    actions = ["publish_selected", "hide_selected"]
    fieldsets = (
        ("Project", {"fields": ("title", "description", "category", "project_type", "tech_tags", "live_url"),
                     "description": "Label the project honestly: client work, internal project or concept demo."}),
        ("Screenshot", {"fields": ("image", "image_preview"),
                        "description": "Use a 16:10 image (for example 1200 × 750). It is cropped from the top."}),
        ("Visibility", {"fields": ("is_published", "sort_order", "created_at")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        return format_html('<img class="at-thumb" src="{}" alt="">', obj.image.url) if obj.image else "—"

    @admin.display(description="Preview")
    def image_preview(self, obj):
        return format_html('<img class="at-thumb-lg" src="{}" alt="">', obj.image.url) if obj and obj.image else "No image yet."

    @admin.display(description="Status")
    def visibility(self, obj):
        return pill("published" if obj.is_published else "draft", "Visible" if obj.is_published else "Hidden")

    @admin.display(boolean=True, description="Live link")
    def has_link(self, obj):
        return bool(obj.live_url)

    @admin.action(description="Show selected on the site")
    def publish_selected(self, request, qs):
        self.message_user(request, f"{qs.update(is_published=True)} project(s) now visible.", messages.SUCCESS)

    @admin.action(description="Hide selected from the site")
    def hide_selected(self, request, qs):
        self.message_user(request, f"{qs.update(is_published=False)} project(s) hidden.", messages.SUCCESS)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "status_badge", "follow_up_date", "email_status", "created_at")
    list_filter = ("status", "service", "email_status")
    search_fields = ("name", "email", "phone", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "phone", "service", "message", "email_status", "created_at", "reply_links")
    actions = ["mark_contacted", "mark_quoted", "mark_won", "mark_lost"]
    fieldsets = (
        ("Enquiry", {"fields": ("name", "email", "phone", "service", "message", "created_at", "reply_links")}),
        ("Follow-up", {"fields": ("status", "follow_up_date", "notes")}),
        ("System", {"fields": ("email_status",),
                    "description": "Whether the notification email to the team was sent. The enquiry is saved either way."}),
    )

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        return pill(obj.status, obj.get_status_display())

    @admin.display(description="Reply")
    def reply_links(self, obj):
        if not obj.pk:
            return "—"
        links = format_html('<a class="at-link" href="mailto:{}?subject=Re: your enquiry to Archon Tech">Reply by email</a>', obj.email)
        if obj.phone:
            links += format_html(' &nbsp;·&nbsp; <a class="at-link" href="tel:{}">Call {}</a>', obj.phone, obj.phone)
        return links

    def _set(self, request, qs, status):
        self.message_user(request, f"{qs.update(status=status)} lead(s) updated.", messages.SUCCESS)

    @admin.action(description="Mark as Contacted")
    def mark_contacted(self, request, qs): self._set(request, qs, Lead.CONTACTED)

    @admin.action(description="Mark as Quoted")
    def mark_quoted(self, request, qs): self._set(request, qs, Lead.QUOTED)

    @admin.action(description="Mark as Won")
    def mark_won(self, request, qs): self._set(request, qs, Lead.WON)

    @admin.action(description="Mark as Lost")
    def mark_lost(self, request, qs): self._set(request, qs, Lead.LOST)
