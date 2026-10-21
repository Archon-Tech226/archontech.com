from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
from site_app.models import PortfolioProject

PORTFOLIO_SEED = [
    dict(
        title="SDS Food Products",
        description="A South Indian snacks and sweets brand site — warm, traditional feel with a product range, menu, and a clear path to ordering.",
        category=PortfolioProject.WEBSITE,
        tech_tags="HTML, CSS, JavaScript",
        image="portfolio/sds-food-products.png",
        sort_order=1,
    ),
    dict(
        title="Urban Spice Kitchen",
        description="A restaurant website with a bold, editorial look — dark hero, full menu, photo gallery, and direct WhatsApp ordering built in.",
        category=PortfolioProject.WEBSITE,
        tech_tags="HTML, CSS, JavaScript",
        image="portfolio/urban-spice-kitchen.png",
        sort_order=2,
    ),
]

# Older placeholder projects that are no longer shown — removed automatically
# if present, so re-running this command cleans up a database seeded before
# the portfolio was trimmed down to real projects.
RETIRED_TITLES = ["Billing system", "Booking system", "ProChat", "Portfolio website", "Business page"]


class Command(BaseCommand):
    help = (
        "Re-seed the site after a fresh database (e.g. Render's free Postgres resetting "
        "every 30 days): recreates the real portfolio projects, removes old placeholder "
        "ones if present, and prompts for the 2 admin accounts if they don't already exist."
    )

    def handle(self, *args, **options):
        removed, _ = PortfolioProject.objects.filter(title__in=RETIRED_TITLES).delete()
        if removed:
            self.stdout.write(self.style.WARNING(f"Removed {removed} retired placeholder project(s)."))

        created = 0
        for item in PORTFOLIO_SEED:
            obj, was_created = PortfolioProject.objects.get_or_create(
                title=item["title"], defaults=item,
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f"Portfolio: {created} project(s) created, {len(PORTFOLIO_SEED) - created} already existed."
        ))

        call_command("seed_blog_posts", stdout=self.stdout)

        for username in ["abinaya", "janaganandhini"]:
            if not User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(
                    f"No admin account for '{username}' yet. Create one with:\n"
                    f"  python manage.py createsuperuser --username {username}"
                ))
            else:
                self.stdout.write(f"Admin account '{username}' already exists.")
