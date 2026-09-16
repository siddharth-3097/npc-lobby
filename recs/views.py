import json

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .emails import (
    send_contribution_email,
    send_invite_email,
    send_love_email,
    send_welcome_email,
    send_your_list_email,
)
from .models import Invite, Karma, Recommendation, ThankYou

DAILY_THANK_YOU_LIMIT = 2
DAILY_INVITE_LIMIT = 3


def _bad_request(message):
    return JsonResponse({"status": "error", "message": message}, status=400)


@require_GET
def index(request):
    return render(request, "recs/index.html", {"type_choices": Recommendation.TYPE_CHOICES})


@require_GET
def list_view(request):
    recommendations = Recommendation.objects.all()
    return render(
        request,
        "recs/list.html",
        {
            "recommendations": recommendations,
            "type_choices": Recommendation.TYPE_CHOICES,
        },
    )


@require_POST
def submit_recommendation(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _bad_request("Malformed request.")

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    rec_type = (data.get("rec_type") or "").strip()
    other_type_label = (data.get("other_type_label") or "").strip()
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()

    if not all([name, email, rec_type, title, description]):
        return _bad_request("Please fill in every field.")

    try:
        validate_email(email)
    except ValidationError:
        return _bad_request("That email doesn't look right.")

    valid_types = {choice[0] for choice in Recommendation.TYPE_CHOICES}
    if rec_type not in valid_types:
        return _bad_request("Pick a valid recommendation type.")

    if rec_type == Recommendation.TYPE_OTHER and not other_type_label:
        return _bad_request("Tell us what kind of recommendation this is.")

    today = timezone.localdate()
    already_posted = Recommendation.objects.filter(
        email__iexact=email, created_at__date=today
    ).exists()

    if already_posted:
        tomorrow = today + timezone.timedelta(days=1)
        return JsonResponse(
            {
                "status": "duplicate",
                "message": (
                    "You've already shared a recommendation today. We don't want to "
                    "spam the list and we'd rather keep the quality high, so come "
                    "back and share your next one on "
                    f"{tomorrow.strftime('%A, %B %d')}."
                ),
                "next_available": tomorrow.isoformat(),
                "next_available_label": tomorrow.strftime("%A, %B %d"),
            },
            status=200,
        )

    recommendation = Recommendation.objects.create(
        name=name,
        email=email,
        rec_type=rec_type,
        other_type_label=other_type_label if rec_type == Recommendation.TYPE_OTHER else "",
        title=title,
        description=description,
    )
    Karma.add(email)

    contribution_number = Recommendation.objects.filter(email__iexact=email).count()
    if contribution_number == 1:
        send_welcome_email(recommendation)
    else:
        karma_total = Karma.objects.get(email=email.strip().lower()).points
        send_contribution_email(recommendation, contribution_number, karma_total)

    return JsonResponse({"status": "ok", "message": "Thanks! Your recommendation is on the list."})


@require_POST
def send_list(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _bad_request("Malformed request.")

    email = (data.get("email") or "").strip()
    ids = data.get("ids") or []

    if not email:
        return _bad_request("We need an email to send your list to.")

    try:
        validate_email(email)
    except ValidationError:
        return _bad_request("That email doesn't look right.")

    if not ids:
        return _bad_request("Select at least one recommendation first.")

    recommendations = Recommendation.objects.filter(id__in=ids)
    if not recommendations:
        return _bad_request("Couldn't find those recommendations.")

    if not send_your_list_email(email, recommendations):
        return _bad_request("Couldn't send that email — double check the address and try again.")

    return JsonResponse({"status": "ok", "message": f"Sent! Check {email}."})


@require_POST
def thank_you(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _bad_request("Malformed request.")

    recommendation_id = data.get("recommendation_id")
    sender_name = (data.get("sender_name") or "").strip()
    sender_email = (data.get("sender_email") or "").strip()
    message = (data.get("message") or "").strip()

    if not recommendation_id or not sender_name or not sender_email:
        return _bad_request("We need your name and email to send the thank you.")

    try:
        validate_email(sender_email)
    except ValidationError:
        return _bad_request("That email doesn't look right.")

    try:
        recommendation = Recommendation.objects.get(id=recommendation_id)
    except Recommendation.DoesNotExist:
        return _bad_request("Couldn't find that recommendation.")

    today = timezone.localdate()
    thanks_today = ThankYou.objects.filter(
        sender_email__iexact=sender_email, created_at__date=today
    ).count()

    if thanks_today >= DAILY_THANK_YOU_LIMIT:
        tomorrow = today + timezone.timedelta(days=1)
        return JsonResponse(
            {
                "status": "duplicate",
                "message": (
                    f"You've already sent {DAILY_THANK_YOU_LIMIT} thank-yous today. "
                    "We cap it there so it stays meaningful — come back and spread "
                    f"more love on {tomorrow.strftime('%A, %B %d')}."
                ),
            },
            status=200,
        )

    ThankYou.objects.create(
        recommendation=recommendation,
        sender_name=sender_name,
        sender_email=sender_email,
        message=message,
    )
    Karma.add(sender_email)
    send_love_email(recommendation, sender_name)

    return JsonResponse({"status": "ok", "message": "Thank you sent!"})


@require_POST
def invite_friend(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _bad_request("Malformed request.")

    inviter_name = (data.get("inviter_name") or "").strip()
    inviter_email = (data.get("inviter_email") or "").strip()
    friend_name = (data.get("friend_name") or "").strip()
    friend_email = (data.get("friend_email") or "").strip()

    if not all([inviter_name, inviter_email, friend_name, friend_email]):
        return _bad_request("Please fill in every field.")

    try:
        validate_email(inviter_email)
        validate_email(friend_email)
    except ValidationError:
        return _bad_request("One of those emails doesn't look right.")

    today = timezone.localdate()
    invites_today = Invite.objects.filter(
        inviter_email__iexact=inviter_email, created_at__date=today
    ).count()

    if invites_today >= DAILY_INVITE_LIMIT:
        tomorrow = today + timezone.timedelta(days=1)
        return JsonResponse(
            {
                "status": "duplicate",
                "message": (
                    f"You've already invited {DAILY_INVITE_LIMIT} friends today. We "
                    "cap it there so it doesn't turn into spam — invite more on "
                    f"{tomorrow.strftime('%A, %B %d')}."
                ),
            },
            status=200,
        )

    invite = Invite.objects.create(
        inviter_name=inviter_name,
        inviter_email=inviter_email,
        friend_name=friend_name,
        friend_email=friend_email,
    )
    Karma.add(inviter_email)
    send_invite_email(invite)

    return JsonResponse({"status": "ok", "message": f"Invite sent to {friend_name}!"})


@require_POST
def check_karma(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _bad_request("Malformed request.")

    email = (data.get("email") or "").strip()

    if not email:
        return _bad_request("We need an email to check.")

    try:
        validate_email(email)
    except ValidationError:
        return _bad_request("That email doesn't look right.")

    karma = Karma.objects.filter(email=email.lower()).first()
    points = karma.points if karma else 0

    return JsonResponse({"status": "ok", "points": points})
