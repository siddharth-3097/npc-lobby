from django.db import migrations

TEASERS = {
    10: "can't wait for you to join our discord",
    50: "your coffee is waiting",
    100: "do you already have a movie in mind?",
    250: "send me your 3 favorite movies",
    500: "any book in mind that you want me to get for you",
    750: "we're already getting your merch printed",
    1000: "i read through your suggestions, i've the perfect vinyl for you",
    1500: "i have no words, im heading to the store to get you what fits you the best",
}


def seed_teasers(apps, schema_editor):
    KarmaTier = apps.get_model("recs", "KarmaTier")
    for threshold, teaser in TEASERS.items():
        KarmaTier.objects.filter(threshold=threshold).update(email_teaser=teaser)


def unseed_teasers(apps, schema_editor):
    KarmaTier = apps.get_model("recs", "KarmaTier")
    KarmaTier.objects.filter(threshold__in=TEASERS.keys()).update(email_teaser="")


class Migration(migrations.Migration):

    dependencies = [
        ("recs", "0007_karmatier_email_teaser"),
    ]

    operations = [
        migrations.RunPython(seed_teasers, unseed_teasers),
    ]
