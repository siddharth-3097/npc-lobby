from .emails import send_weekly_tier_progress_email
from .models import Invite, Karma, KarmaTier, Recommendation, ThankYou


def _display_name(email):
    email = email.strip().lower()
    rec = Recommendation.objects.filter(email__iexact=email).order_by("-created_at").first()
    if rec:
        return rec.name
    thank_you = ThankYou.objects.filter(sender_email__iexact=email).order_by("-created_at").first()
    if thank_you:
        return thank_you.sender_name
    invite = Invite.objects.filter(inviter_email__iexact=email).order_by("-created_at").first()
    if invite:
        return invite.inviter_name
    return email.split("@")[0]


def send_weekly_tier_progress_emails():
    """Email everyone with karma how far they are from their next tier.

    Skips anyone already past the highest configured tier.
    """
    tiers = list(KarmaTier.objects.order_by("threshold"))
    sent = 0
    for karma in Karma.objects.all():
        next_tier = next((tier for tier in tiers if tier.threshold > karma.points), None)
        if next_tier is None:
            continue
        points_away = next_tier.threshold - karma.points
        name = _display_name(karma.email)
        ok = send_weekly_tier_progress_email(
            karma.email, name, points_away, next_tier.tier_name, next_tier.email_teaser
        )
        if ok:
            sent += 1
    return sent
