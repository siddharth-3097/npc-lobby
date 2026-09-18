import logging

import resend
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import escape

logger = logging.getLogger(__name__)


def _html_document(paragraphs_html):
    """Wrap a list of already-formatted HTML paragraph strings in a plain,
    unbranded shell — just spacing and a readable font, no logo/colors/
    buttons.
    """
    body = "".join(f'<p style="margin:0 0 16px 0;">{p}</p>' for p in paragraphs_html)
    return (
        '<div style="font-family:-apple-system,BlinkMacSystemFont,'
        "'Segoe UI',Helvetica,Arial,sans-serif;"
        'font-size:15px;line-height:1.65;color:#111111;">'
        f"{body}"
        "</div>"
    )


def send_email(to, subject, text, html=None):
    """Send an email, but never let a delivery failure break the request
    that triggered it — these are side-effect notifications, not the core
    action (creating a recommendation, thanking someone, etc).
    """
    try:
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY
            payload = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [to],
                "subject": subject,
                "text": text,
            }
            if html:
                payload["html"] = html
            resend.Emails.send(payload)
        elif html:
            message = EmailMultiAlternatives(
                subject=subject,
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to],
            )
            message.attach_alternative(html, "text/html")
            message.send(fail_silently=False)
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
    name = recommendation.name
    text = (
        f"hi {name}- you made your first recommendation to NPC Lobby. thanks 🎉\n\n"
        "there's no such thing as a \"superior\" list, but there is definitely a loved list\n\n"
        "Over the coming weeks, I hope we get to see more of your taste here 👀\n\n"
        "+1 karma from me ✨"
    )
    html = _html_document([
        f"hi {escape(name)}- you made your first recommendation to NPC Lobby. thanks 🎉",
        "there's no such thing as a <em>\"superior\"</em> list, but there is definitely a <strong>loved</strong> list.",
        "Over the coming weeks, I hope we get to see more of your taste here 👀",
        "<strong>+1 karma</strong> from me ✨",
    ])
    return send_email(recommendation.email, subject, text, html)


def send_contribution_email(recommendation, contribution_number, karma_total):
    subject = "thanks for your contribution"
    name = recommendation.name
    title = recommendation.title
    text = (
        f"hi {name} - 👋\n\n"
        f"thanks for recommendation #{contribution_number}\n\n"
        f"+1 karma for {title} 🌟\n\n"
        f"you have collected {karma_total} so far. hope to see more from you tomorrow 🙌"
    )
    html = _html_document([
        f"hi {escape(name)} - 👋",
        f"thanks for recommendation <strong>#{contribution_number}</strong>",
        f"<strong>+1 karma</strong> for <em>{escape(title)}</em> 🌟",
        f"you have collected <strong>{karma_total}</strong> so far. hope to see more from you tomorrow 🙌",
    ])
    return send_email(recommendation.email, subject, text, html)


def send_love_email(recommendation, liker_name):
    subject = "you got a like"
    name = recommendation.name
    title = recommendation.title
    text = (
        f"hi {name} ❤️\n\n"
        f"{liker_name} liked your recommendation- {title}\n\n"
        "keep them coming! Cheers 🙌"
    )
    html = _html_document([
        f"hi {escape(name)} ❤️",
        f"<strong>{escape(liker_name)}</strong> liked your recommendation- <em>{escape(title)}</em>",
        "keep them coming! Cheers 🙌",
    ])
    return send_email(recommendation.email, subject, text, html)


def send_thank_you_confirmation_email(sender_name, sender_email, karma_total):
    subject = "you just earned karma"
    text = (
        f"hey {sender_name}- to like is human, to thank divine. 🙏\n\n"
        "+1 karma for u, for appreciating someone's taste ✨\n\n"
        f"your karma balance is now {karma_total} 🎉"
    )
    html = _html_document([
        f"hey {escape(sender_name)}- <em>to like is human, to thank divine</em>. 🙏",
        "<strong>+1 karma</strong> for u, for appreciating someone's taste ✨",
        f"your karma balance is now <strong>{karma_total}</strong> 🎉",
    ])
    return send_email(sender_email, subject, text, html)


def send_invite_email(invite):
    subject = "you have been invited to NPC Lobby"
    friend_name = invite.friend_name
    inviter_name = invite.inviter_name
    site_url = settings.SITE_URL
    text = (
        f"hey {friend_name} 👋\n\n"
        f"{inviter_name} told me that you have a lot of cool stuff to share\n\n"
        f"NPC Lobby is waiting for it, dying for it- pls join in here {site_url}"
    )
    html = _html_document([
        f"hey {escape(friend_name)} 👋",
        f"<strong>{escape(inviter_name)}</strong> told me that you have a lot of cool stuff to share",
        f"NPC Lobby is <em>waiting for it, dying for it</em>- pls join in here "
        f'<a href="{escape(site_url)}">{escape(site_url)}</a> 🚪',
    ])
    return send_email(invite.friend_email, subject, text, html)


def send_weekly_tier_progress_email(email, name, points_away, tier_name, teaser):
    subject = f"you're closer to {tier_name}"
    text = (
        f"hey {name}, thanks for making NPC Lobby tasteful. "
        f"you're {points_away} karma points away from {tier_name}. "
        f"{teaser}"
    )
    html = _html_document([
        f"hey {escape(name)}, thanks for making NPC Lobby tasteful. "
        f"you're <strong>{points_away}</strong> karma points away from <strong>{tier_name}</strong>. "
        f"<em>{escape(teaser)}</em>"
    ])
    return send_email(email, subject, text, html)


def send_your_list_email(email, recommendations):
    lines = ["Here's your NPC Lobby list: 📋\n"]
    for rec in recommendations:
        lines.append(f"- {rec.title} ({rec.get_type_label()})")
        lines.append(f"  {rec.description}")
        lines.append("")
    text = "\n".join(lines)

    paragraphs = ["Here's your <strong>NPC Lobby</strong> list: 📋"]
    for rec in recommendations:
        paragraphs.append(
            f"<strong>{escape(rec.title)}</strong> <em>({escape(rec.get_type_label())})</em>"
            f"<br>{escape(rec.description)}"
        )
    html = _html_document(paragraphs)

    return send_email(email, "Your NPC Lobby List", text, html)
