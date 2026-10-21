from django.core.management.base import BaseCommand
from site_app.content import SAMPLE_TESTIMONIALS
from site_app.models import Testimonial


class Command(BaseCommand):
    help = ("Create three clearly labelled SAMPLE testimonials for local development only. "
            "They are flagged is_sample and are never shown publicly when DEBUG is off. Safe to re-run.")

    def handle(self, *args, **options):
        created = 0
        for name, company, quote in SAMPLE_TESTIMONIALS:
            _, ok = Testimonial.objects.get_or_create(
                client_name=name, is_sample=True,
                defaults=dict(company=company, quote=quote, rating=5, is_published=True))
            created += ok
        self.stdout.write(self.style.SUCCESS(f"Sample testimonials: {created} created."))
