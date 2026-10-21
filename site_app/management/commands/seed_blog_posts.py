from django.core.management.base import BaseCommand
from site_app.content import BLOG_POSTS
from site_app.models import BlogPost


class Command(BaseCommand):
    help = "Create the three default Behind the Build articles. Safe to re-run: existing posts (matched by slug) are never changed."

    def handle(self, *args, **options):
        created = 0
        for item in BLOG_POSTS:
            _, was_created = BlogPost.objects.get_or_create(
                slug=item["slug"],
                defaults=dict(
                    title=item["title"], category=item["category"], excerpt=item["excerpt"],
                    body=item["body"], author_name="Archon Tech", status=BlogPost.PUBLISHED,
                ),
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(
            f"Blog: {created} created, {len(BLOG_POSTS) - created} already existed (left untouched)."))
