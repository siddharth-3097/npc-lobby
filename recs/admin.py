from django.contrib import admin

from .models import Invite, Karma, KarmaTier, Recommendation, ThankYou


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("title", "rec_type", "name", "email", "created_at")
    list_filter = ("rec_type", "created_at")
    search_fields = ("title", "name", "email", "description")


@admin.register(ThankYou)
class ThankYouAdmin(admin.ModelAdmin):
    list_display = ("recommendation", "sender_name", "sender_email", "created_at")
    search_fields = ("sender_name", "sender_email", "message")


@admin.register(Karma)
class KarmaAdmin(admin.ModelAdmin):
    list_display = ("email", "points", "updated_at")
    search_fields = ("email",)
    ordering = ("-points",)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("inviter_name", "inviter_email", "friend_name", "friend_email", "created_at")
    search_fields = ("inviter_name", "inviter_email", "friend_name", "friend_email")


@admin.register(KarmaTier)
class KarmaTierAdmin(admin.ModelAdmin):
    list_display = ("threshold", "tier_name", "unlock_text")
    ordering = ("threshold",)
    list_editable = ("tier_name", "unlock_text")
