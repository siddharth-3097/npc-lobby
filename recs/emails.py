import logging

import resend
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email(to, subject, text):
    """Send an email, but never let a delivery failure break the request
    that triggered it — these are side-effect notifications, not the core
    action (creating a recommendation, thanking someone, etc).
    """
    try:
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [to],
                "subject": subject,
                "text": text,
            })
        else:
            send_mail(
                subject=subject,
                message=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to],
                fail_silently=False,
            )
        return True
    except Exception:
        logger.exception("Failed to send email %r to %s", subject, to)
        return False


def send_welcome_email(recommendation):
    subject = "welcome npc"
    text = (
        f"hi {recommendation.name}- you made your first recommendation to NPC Lobby. thanks\n\n"
        "there's no such thing as a \"superior\" list, but there is definitely a loved list\n\n"
        "Over the coming weeks, I hope we get to see more of your taste here\n\n"
        "+1 karma from me"
    )
    send_email(recommendation.email, subject, text)


def send_contribution_email(recommendation, contribution_number, karma_total):
    subject = "thanks for your contribution"
    text = (
        f"hi {recommendation.name} - \n\n"
        f"thanks for recommendation #{contribution_number}\n\n"
        f"+1 karma for {recommendation.title}\n\n"
        f"you have collected {karma_total} so far. hope to see more from you tomorrow"
    )
    send_email(recommendation.email, subject, text)


def send_love_email(recommendation, liker_name):
    subject = "you got a like"
    text = (
        f"hi {recommendation.name}\n\n"
        f"{liker_name} liked your recommendation- {recommendation.title}\n\n"
        "keep them coming! Cheers"
    )
    send_email(recommendation.email, subject, text)


def send_invite_email(invite):
    subject = "you have been invited to NPC Lobby"
    text = (
        f"hey {invite.friend_name}\n\n"
        f"{invite.inviter_name} told me that you have a lot of cool stuff to share\n\n"
        f"NPC Lobby is waiting for it, dying for it- pls join in here {settings.SITE_URL}"
    )
    send_email(invite.friend_email, subject, text)


def send_your_list_email(email, recommendations):
    lines = ["Here's your NPC Lobby list:\n"]
    for rec in recommendations:
        lines.append(f"- {rec.title} ({rec.get_type_label()})")
        lines.append(f"  {rec.description}")
        lines.append("")

    return send_email(email, "Your NPC Lobby List", "\n".join(lines))
