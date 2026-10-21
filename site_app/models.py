from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class BlogPost(models.Model):
    """A "Behind the Build" note, written by a signed-in team member."""

    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    author_name = models.CharField(
        max_length=80,
        help_text="Name shown on the post (e.g. 'Abinaya Sri'). Separate from the login account.",
    )
    title = models.CharField(max_length=160, blank=True, help_text="Leave blank for a short note.")
    slug = models.SlugField(max_length=160, unique=True, null=True, blank=True,
                            help_text="Used in the article URL. Auto-filled from the title if blank.")
    category = models.CharField(max_length=60, blank=True)
    excerpt = models.CharField(max_length=300, blank=True)
    body = models.TextField(
        help_text="Plain text. Start a line with '## ' for a heading and '- ' for a bullet.",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"{self.author_name}: {self.body[:40]}"

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            base = slugify(self.title)[:150] or "post"
            slug, n = base, 2
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_post", args=[self.slug]) if self.slug else reverse("blog")

    @property
    def is_article(self):
        return bool(self.title and self.slug)


class Testimonial(models.Model):
    """A client testimonial, added by an admin — never submitted by clients directly."""

    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    quote = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    is_published = models.BooleanField(default=True)
    is_sample = models.BooleanField(
        default=False,
        help_text="Development-only placeholder. Never shown publicly when DEBUG is off.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} ({self.rating}\u2605)"

    def stars(self):
        return "\u2605" * self.rating + "\u2606" * (5 - self.rating)


class PortfolioProject(models.Model):
    """A project shown on the Portfolio page."""

    WEBSITE = "website"
    APP = "app"
    CATEGORY_CHOICES = [(WEBSITE, "Website"), (APP, "Web application")]

    CLIENT = "client"
    INTERNAL = "internal"
    CONCEPT = "concept"
    PROJECT_TYPE_CHOICES = [
        ("", "Not labelled yet"),
        (CLIENT, "Client work"),
        (INTERNAL, "Internal project"),
        (CONCEPT, "Concept / demo"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPE_CHOICES, blank=True, default="",
                                    help_text="Be accurate: never label a demo as client work.")
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=APP)
    tech_tags = models.CharField(
        max_length=200,
        help_text="Comma-separated, e.g. 'Python, Django, MySQL'",
        blank=True,
    )
    live_url = models.URLField(blank=True, help_text="Leave blank if not deployed yet")
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tech_tags.split(",") if t.strip()]


class Lead(models.Model):
    """A contact-form submission."""

    NEW = "new"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    WON = "won"
    LOST = "lost"
    STATUS_CHOICES = [
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (QUOTED, "Quoted"),
        (WON, "Won"),
        (LOST, "Lost"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=100, blank=True)
    message = models.TextField(max_length=2000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)
    notes = models.TextField(blank=True, help_text="Internal notes, not shown to the client")
    follow_up_date = models.DateField(null=True, blank=True)
    EMAIL_NOT_CONFIGURED = "not_configured"
    EMAIL_SENT = "sent"
    EMAIL_FAILED = "failed"
    EMAIL_CHOICES = [(EMAIL_NOT_CONFIGURED, "Email not configured"), (EMAIL_SENT, "Notification sent"),
                     (EMAIL_FAILED, "Notification failed")]
    email_status = models.CharField(max_length=14, choices=EMAIL_CHOICES, default=EMAIL_NOT_CONFIGURED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} \u2014 {self.get_status_display()}"
