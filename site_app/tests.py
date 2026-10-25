from unittest import mock

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .content import BLOG_POSTS
from .models import BlogPost, Lead, Testimonial


class PublicPagesTests(TestCase):
    def test_all_public_pages_load(self):
        for name in ["home", "services", "portfolio", "about", "team", "contact", "blog"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_404_is_real_404(self):
        with override_settings(DEBUG=False):
            r = self.client.get("/definitely-not-a-page/")
        self.assertEqual(r.status_code, 404)
        self.assertContains(r, "Back to home", status_code=404)

    def test_nav_has_blog_and_active_state(self):
        r = self.client.get(reverse("blog"))
        self.assertContains(r, 'aria-current="page">Blog')

    def test_four_services_everywhere(self):
        for url in [reverse("home"), reverse("services")]:
            html = self.client.get(url).content.decode()
            for name in ["Web Development", "Social Media Marketing", "Web Applications", "SaaS Products"]:
                self.assertIn(name, html, f"{name} missing on {url}")

    def test_about_uses_logo_not_portrait_and_team_has_portrait(self):
        about = self.client.get(reverse("about")).content.decode()
        team = self.client.get(reverse("team")).content.decode()
        self.assertIn("logo13", about)
        self.assertNotIn("founder.png", about)
        self.assertIn("founder.png", team)

    def test_dark_is_default_theme(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertNotIn('data-theme="light"></html', html)
        self.assertIn('getItem("archon-theme") === "light"', html)  # light only on explicit saved choice
        self.assertIn("theme-toggle", html)


class BlogSeedTests(TestCase):
    def test_seed_is_idempotent_and_preserves_edits(self):
        call_command("seed_blog_posts", verbosity=0)
        self.assertEqual(BlogPost.objects.filter(slug__isnull=False).count(), 3)
        post = BlogPost.objects.get(slug=BLOG_POSTS[0]["slug"])
        post.title = "My edited title"
        post.save()
        call_command("seed_blog_posts", verbosity=0)
        self.assertEqual(BlogPost.objects.filter(slug__isnull=False).count(), 3)
        post.refresh_from_db()
        self.assertEqual(post.title, "My edited title")

    def test_detail_pages_and_draft_hidden(self):
        call_command("seed_blog_posts", verbosity=0)
        for item in BLOG_POSTS:
            r = self.client.get(reverse("blog_post", args=[item["slug"]]))
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, item["title"].split(":")[0][:20])
        BlogPost.objects.filter(slug=BLOG_POSTS[0]["slug"]).update(status=BlogPost.DRAFT)
        self.assertEqual(self.client.get(reverse("blog_post", args=[BLOG_POSTS[0]["slug"]])).status_code, 404)

    def test_body_is_escaped(self):
        BlogPost.objects.create(author_name="T", title="X", body="<script>alert(1)</script>", status="published")
        r = self.client.get(BlogPost.objects.get(title="X").get_absolute_url())
        self.assertNotContains(r, "<script>alert(1)</script>")


class TestimonialSafetyTests(TestCase):
    def setUp(self):
        call_command("seed_sample_testimonials", verbosity=0)

    @override_settings(DEBUG=False)
    def test_samples_never_public_in_production(self):
        r = self.client.get(reverse("home"))
        self.assertNotContains(r, "SAMPLE")
        self.assertNotContains(r, "What clients say")

    @override_settings(DEBUG=True)
    def test_samples_labelled_in_development(self):
        r = self.client.get(reverse("home"))
        self.assertContains(r, "SAMPLE, DEVELOPMENT ONLY", count=3)

    @override_settings(DEBUG=False)
    def test_real_testimonial_shows(self):
        Testimonial.objects.create(client_name="Real Person", quote="Genuine approved quote", is_published=True)
        self.assertContains(self.client.get(reverse("home")), "Genuine approved quote")

    def test_seed_is_idempotent(self):
        call_command("seed_sample_testimonials", verbosity=0)
        self.assertEqual(Testimonial.objects.filter(is_sample=True).count(), 3)


class ContactTests(TestCase):
    data = {"name": "Ana", "email": "ana@example.com", "phone": "", "service": "Web Application",
            "message": "Need a booking tool", "company_website": ""}

    def test_invalid_post_shows_errors_and_saves_nothing(self):
        r = self.client.post(reverse("contact"), {**self.data, "email": "nope"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "not been sent")
        self.assertEqual(Lead.objects.count(), 0)

    def test_phone_optional_and_saved(self):
        self.client.post(reverse("contact"), self.data)
        self.assertEqual(Lead.objects.get().email_status, Lead.EMAIL_NOT_CONFIGURED)

    @override_settings(EMAIL_HOST_USER="x@example.com")
    def test_email_failure_keeps_lead_and_records_failure(self):
        with mock.patch("site_app.views.send_mail", side_effect=OSError("smtp down")):
            r = self.client.post(reverse("contact"), self.data, follow=True)
        lead = Lead.objects.get()
        self.assertEqual(lead.email_status, Lead.EMAIL_FAILED)
        self.assertNotContains(r, "email was sent")
        self.assertEqual(r.status_code, 200)

    def test_service_prefill(self):
        r = self.client.get(reverse("contact") + "?service=SaaS%20Product")
        self.assertContains(r, 'value="SaaS Product" selected')

    def test_honeypot(self):
        self.client.post(reverse("contact"), {**self.data, "company_website": "spam"})
        self.assertEqual(Lead.objects.count(), 0)


class DashboardTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", password="pw-for-tests-123", is_staff=True)

    def test_requires_login(self):
        self.assertEqual(self.client.get(reverse("dashboard:home")).status_code, 302)

    def test_pages_load_when_logged_in(self):
        call_command("seed_blog_posts", verbosity=0)
        Lead.objects.create(name="A", email="a@example.com", message="m")
        self.client.force_login(self.staff)
        for name in ["home", "leads_list", "blog_list", "blog_add", "testimonial_list", "testimonial_add",
                     "portfolio_list", "portfolio_add"]:
            self.assertEqual(self.client.get(reverse(f"dashboard:{name}")).status_code, 200, name)
        lead = Lead.objects.get()
        self.assertEqual(self.client.get(reverse("dashboard:lead_detail", args=[lead.pk])).status_code, 200)

    def test_lead_followup_saves_without_htmx(self):
        lead = Lead.objects.create(name="A", email="a@example.com", message="m")
        self.client.force_login(self.staff)
        r = self.client.post(reverse("dashboard:lead_detail", args=[lead.pk]),
                             {"status": "contacted", "follow_up_date": "2026-11-01", "notes": "called"})
        self.assertEqual(r.status_code, 302)
        lead.refresh_from_db()
        self.assertEqual(str(lead.follow_up_date), "2026-11-01")


class AdminLiveDashboardTests(TestCase):
    def setUp(self):
        self.su = User.objects.create_superuser("boss", "b@example.com", "pw-for-tests-123")
        self.lead = Lead.objects.create(name="Ana", email="a@example.com", message="hi")

    def test_endpoints_require_staff(self):
        self.assertEqual(self.client.get(reverse("admin_live_stats")).status_code, 302)
        r = self.client.post(reverse("admin_lead_status"), "{}", content_type="application/json")
        self.assertEqual(r.status_code, 302)

    def test_stats_and_status_update(self):
        self.client.force_login(self.su)
        data = self.client.get(reverse("admin_live_stats") + "?days=7").json()
        self.assertEqual(data["cards"]["leads_total"], 1)
        self.assertEqual(len(data["series"]), 7)
        r = self.client.post(reverse("admin_lead_status"), '{"id": %d, "status": "contacted"}' % self.lead.pk,
                             content_type="application/json")
        self.assertTrue(r.json()["ok"])
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, "contacted")
        bad = self.client.post(reverse("admin_lead_status"), '{"id": %d, "status": "hacked"}' % self.lead.pk,
                               content_type="application/json")
        self.assertEqual(bad.status_code, 400)

    def test_admin_home_renders_dashboard(self):
        self.client.force_login(self.su)
        self.assertContains(self.client.get("/admin/"), 'id="live-dash"')


class AdminThemeAndCalendarTests(TestCase):
    def setUp(self):
        self.su = User.objects.create_superuser("boss2", "b@example.com", "pw-for-tests-123")
        self.lead = Lead.objects.create(name="Cal", email="c@example.com", message="hi")

    def test_login_page_is_custom(self):
        r = self.client.get("/admin/login/")
        self.assertContains(r, "Welcome back")
        self.assertContains(r, 'id="lg-toggle"')

    def test_every_model_screen_renders(self):
        self.client.force_login(self.su)
        call_command("seed_blog_posts", verbosity=0)
        call_command("seed_sample_testimonials", verbosity=0)
        for m in ["blogpost", "testimonial", "portfolioproject", "lead"]:
            self.assertEqual(self.client.get(f"/admin/site_app/{m}/").status_code, 200, m)
            self.assertEqual(self.client.get(f"/admin/site_app/{m}/add/").status_code, 200, m)
        post = BlogPost.objects.first()
        self.assertEqual(self.client.get(f"/admin/site_app/blogpost/{post.pk}/change/").status_code, 200)
        self.assertEqual(self.client.get(f"/admin/site_app/lead/{self.lead.pk}/change/").status_code, 200)
        self.assertContains(self.client.get("/admin/site_app/lead/"), "Mark as Won")

    def test_calendar_endpoints(self):
        self.client.force_login(self.su)
        from django.utils import timezone
        today = timezone.localdate()
        m = self.client.get(reverse("admin_calendar") + f"?month={today.year}-{today.month:02d}").json()
        self.assertEqual(m["days"][str(today.day)]["leads"], 1)
        d = self.client.get(reverse("admin_calendar_day") + f"?date={today.isoformat()}").json()
        self.assertEqual(len(d["items"]), 1)
        self.assertEqual(self.client.get(reverse("admin_calendar_day") + "?date=bad").status_code, 400)

    def test_calendar_requires_staff(self):
        self.assertEqual(self.client.get(reverse("admin_calendar")).status_code, 302)
