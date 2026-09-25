from django.db import migrations

# Hand-researched thumbnail + access links for the recommendations that
# existed at the time this feature shipped. New recommendations start
# blank until someone fills them in via the admin.
MEDIA_LINKS = {
    5: (
        "https://upload.wikimedia.org/wikipedia/en/2/2a/Perfectblueposter.png",
        "https://www.amazon.com/Perfect-Blue-Junko-Iwao/dp/B07NNP4R4H",
    ),
    6: (
        "https://upload.wikimedia.org/wikipedia/en/0/08/Hot_Wheels_logo-en.svg",
        "https://shop.mattel.com/collections/hot-wheels",
    ),
    8: (
        "https://images.justwatch.com/poster/230881223/s166/la-frecuencia-kirlian.jpg",
        "https://www.netflix.com/title/81045308",
    ),
    9: (
        "https://archive.org/services/img/capitaleruptiono0000dasg",
        "https://archive.org/details/capitaleruptiono0000dasg",
    ),
    10: (
        "https://books.google.com/books/content?id=KW9fEQAAQBAJ&printsec=frontcover&img=1&zoom=1",
        "https://www.amazon.com/Meet-Savarnas-Millennials-Mediocrity-Everything/dp/0143465716",
    ),
    14: (
        "https://thumb.wikimedia.org/wikipedia/en/thumb/7/77/Solanin_vol.1.png/250px-Solanin_vol.1.png",
        "https://www.overdrive.com/media/4247525/solanin",
    ),
    15: (
        "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Average_White_Pillow.jpg/250px-Average_White_Pillow.jpg",
        "https://www.amazon.com/s?k=bed+pillows",
    ),
    16: (
        "https://upload.wikimedia.org/wikipedia/en/1/16/Little_miss_sunshine_poster.jpg",
        "https://www.netflix.com/title/70043947",
    ),
    17: (
        "https://www.gutenberg.org/cache/epub/18857/pg18857.cover.medium.jpg",
        "https://www.gutenberg.org/ebooks/18857",
    ),
    18: (
        "https://thumb.wikimedia.org/wikipedia/en/thumb/4/4e/Netflix_Fall_of_House_of_Usher_series.png/250px-Netflix_Fall_of_House_of_Usher_series.png",
        "https://www.netflix.com/title/81414665",
    ),
    19: (
        "https://thumb.wikimedia.org/wikipedia/en/thumb/1/14/Sangatsu_no_Lion.jpg/250px-Sangatsu_no_Lion.jpg",
        "https://www.crunchyroll.com/series/GRVNXWQZY/march-comes-in-like-a-lion",
    ),
}


def seed_media_links(apps, schema_editor):
    Recommendation = apps.get_model("recs", "Recommendation")
    for rec_id, (thumbnail_url, access_url) in MEDIA_LINKS.items():
        Recommendation.objects.filter(id=rec_id).update(
            thumbnail_url=thumbnail_url, access_url=access_url
        )


def unseed_media_links(apps, schema_editor):
    Recommendation = apps.get_model("recs", "Recommendation")
    Recommendation.objects.filter(id__in=MEDIA_LINKS.keys()).update(
        thumbnail_url="", access_url=""
    )


class Migration(migrations.Migration):

    dependencies = [
        ("recs", "0009_recommendation_access_url_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_media_links, unseed_media_links),
    ]
