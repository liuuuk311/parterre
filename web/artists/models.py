from random import randint
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet, Max

from utils.models import TimestampedModel, UUIDModel


def restrict_number_of_users_per_artist(value):
    if Artist.objects.filter(user_id=value).count() >= 1:
        raise ValidationError('Artist has already a user')


class Artist(UUIDModel, TimestampedModel):
    spotify_url = models.URLField(max_length=256)
    image = models.ImageField(null=True, blank=True, default=None)
    stage_name = models.CharField(max_length=256, null=True, blank=True, default=None)
    bio = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(
        "Verified at", default=None, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        validators=(restrict_number_of_users_per_artist,),
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )
    force_visible = models.BooleanField(default=False)
    genres = models.ManyToManyField("Genre", related_name="artists", blank=True)

    def __str__(self):
        if self.stage_name:
            return f"{self.stage_name}"

        return f"No name yet ({self.spotify_id})"

    def get_percentage(self):
        if self.popularity_history.count() < 2:
            return 0
        this_week, last_week = self.popularity_history.all()[:2]
        return round(last_week.parterre_score / this_week.parterre_score * 100 - 100, 2)

    @property
    def reviews(self):
        return Artist.objects.none()

    @property
    def current_price(self):
        if self.popularity_history.count() == 0:
            return 0

        return round(self.popularity_history.last().parterre_score * 10)

    @property
    def spotify_id(self):
        url = urlparse(self.spotify_url)
        return url.path.split('/')[-1]

    @property
    def tracks(self):
        return Track.objects.filter(artists=self)

    @property
    def is_visible(self):
        # TODO: Capire cosa fare quando Aritsta scompare ed in una label
        if self.force_visible:
            return True
        return (
            self.popularity_history.aggregate(Max("parterre_score"))
            and self.popularity_history.last().parterre_score < 8
        )

    @property
    def genre_name_list(self):
        return ', '.join([genre.name for genre in self.genres.all()])


class Profile(models.Model):
    SOCIAL_MEDIA_CHOICES = (
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("spotify", "Spotify"),
        ("soundcloud", "SoundCloud"),
    )

    name = models.CharField(max_length=64, choices=SOCIAL_MEDIA_CHOICES)
    url = models.URLField("Link")
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="other_profiles"
    )


class ArtistPopularity(models.Model):
    spotify_popularity = models.IntegerField()
    spotify_followers = models.BigIntegerField()
    monthly_listeners = models.BigIntegerField()
    parterre_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(
        Artist, null=False, related_name="popularity_history", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)

    @classmethod
    def compute_parterre_score(
        cls, spotify_popularity, spotify_followers, monthly_listeners
    ) -> float:
        return (
            (spotify_popularity / 100 * 4)
            + (spotify_followers / 30000 * 2)
            + (monthly_listeners / 500000 * 4)
        )


class Track(UUIDModel):
    spotify_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    artists = models.ManyToManyField(Artist)

    @property
    def popularity(self):
        last_pop = self.popularity_history.last()
        return (
            last_pop.spotify_popularity * self.playlist_set.count() if last_pop else 0
        )

    @property
    def percentage_over_last_week(self):
        if self.popularity_history.count() < 2:
            return None

        current_popularity = self.popularity_history.all().order_by('-created_at')[0]
        last_week_popularity = self.popularity_history.all().order_by('-created_at')[1]
        return (
            (max(current_popularity.spotify_plays, 1) - max(last_week_popularity.spotify_plays, 1))
            / max(last_week_popularity.spotify_plays, 1) * 100
        )


class TrackPopularity(models.Model):
    spotify_popularity = models.IntegerField()
    spotify_plays = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(
        Track, null=False, related_name="popularity_history", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)


class Genre(UUIDModel):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
