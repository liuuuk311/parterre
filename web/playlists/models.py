from urllib.parse import urlparse

from django.db import models

from artists.models import Track


class Playlist(models.Model):
    spotify_url = models.URLField(max_length=256)
    name = models.CharField(max_length=256, null=True, blank=True, default=None)
    followers = models.IntegerField(null=True, blank=True, default=None)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return self.name or "No name yet"

    @property
    def spotify_id(self):
        url = urlparse(self.spotify_url)
        return url.path.split('/')[-1]
