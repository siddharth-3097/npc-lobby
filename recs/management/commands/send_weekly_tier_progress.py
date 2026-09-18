from django.core.management.base import BaseCommand

from recs.tier_progress import send_weekly_tier_progress_emails


class Command(BaseCommand):
    help = "Email everyone with karma how many points they need to reach their next tier."

    def handle(self, *args, **options):
        sent = send_weekly_tier_progress_emails()
        self.stdout.write(self.style.SUCCESS(f"Sent {sent} weekly tier-progress emails."))
