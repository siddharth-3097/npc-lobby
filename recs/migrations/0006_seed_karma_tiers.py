from django.db import migrations

TIERS = [
    (10, "Lurker", "\U0001F512 access to our private Discord"),
    (50, "Plug", "☕ your next coffee is our treat"),
    (100, "Scout", "\U0001F3AB your next movie ticket is covered"),
    (250, "Curator", "\U0001F3AC join the team for movie night"),
    (500, "Tastemaker", "\U0001F4DA your next book is on us"),
    (750, "Connoisseur", "\U0001F451 exclusive member merch"),
    (1000, "Cult Figure", "\U0001F4BF our vinyl pick of the month, delivered to you"),
    (1500, "God Tier", "⚡ the ultimate recommendation hamper"),
]


def seed_tiers(apps, schema_editor):
    KarmaTier = apps.get_model("recs", "KarmaTier")
    for threshold, tier_name, unlock_text in TIERS:
        KarmaTier.objects.update_or_create(
            threshold=threshold,
            defaults={"tier_name": tier_name, "unlock_text": unlock_text},
        )


def remove_tiers(apps, schema_editor):
    KarmaTier = apps.get_model("recs", "KarmaTier")
    KarmaTier.objects.filter(threshold__in=[t[0] for t in TIERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("recs", "0005_karmatier"),
    ]

    operations = [
        migrations.RunPython(seed_tiers, remove_tiers),
    ]
