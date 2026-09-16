from django.db import models
from django.utils import timezone


class Recommendation(models.Model):
    TYPE_MOVIE = "movie"
    TYPE_TV = "tv_show"
    TYPE_ANIME = "anime"
    TYPE_BOOK = "book"
    TYPE_PODCAST = "podcast"
    TYPE_GAME = "game"
    TYPE_SUBREDDIT = "subreddit"
    TYPE_IG = "ig_handle"
    TYPE_MUSIC = "music"
    TYPE_OTHER = "other"

    TYPE_CHOICES = [
        (TYPE_MOVIE, "Movie"),
        (TYPE_TV, "TV Show"),
        (TYPE_ANIME, "Anime"),
        (TYPE_BOOK, "Book"),
        (TYPE_PODCAST, "Podcast"),
        (TYPE_GAME, "Game"),
        (TYPE_SUBREDDIT, "Subreddit"),
        (TYPE_IG, "Instagram Handle"),
        (TYPE_MUSIC, "Music"),
        (TYPE_OTHER, "Other"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    rec_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    other_type_label = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=200, help_text="The thing being recommended")
    description = models.TextField(help_text="Who will love it and why")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_type_label()})"

    def get_type_label(self):
        if self.rec_type == self.TYPE_OTHER and self.other_type_label:
            return self.other_type_label
        return self.get_rec_type_display()


class ThankYou(models.Model):
    recommendation = models.ForeignKey(
        Recommendation, related_name="thank_yous", on_delete=models.CASCADE
    )
    sender_name = models.CharField(max_length=120)
    sender_email = models.EmailField(default="")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender_name} -> {self.recommendation.title}"


class Invite(models.Model):
    inviter_name = models.CharField(max_length=120)
    inviter_email = models.EmailField()
    friend_name = models.CharField(max_length=120)
    friend_email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.inviter_name} -> {self.friend_name}"


class Karma(models.Model):
    email = models.EmailField(unique=True)
    points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-points"]
        verbose_name_plural = "karma"

    def __str__(self):
        return f"{self.email}: {self.points}"

    @classmethod
    def add(cls, email, amount=1):
        email = email.strip().lower()
        obj, _ = cls.objects.get_or_create(email=email)
        cls.objects.filter(pk=obj.pk).update(points=models.F("points") + amount)
