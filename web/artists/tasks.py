import time
from urllib.request import urlopen

from celery import shared_task
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

from artists.models import Artist, ArtistPopularity, Track, TrackPopularity
from spotify.clients import SpotifyAPI, SpotifyPartnerAPI

client = SpotifyAPI()
private_client = SpotifyPartnerAPI()


@shared_task
def import_artist_data(artist_ids):
    for artist in Artist.objects.filter(id__in=artist_ids):
        data = client.get_artist(artist.spotify_id)

        if not artist.stage_name:
            artist.stage_name = data.get('name')

        img_temp = NamedTemporaryFile(delete=True)
        with urlopen(data.get('images')[0].get('url')) as response:
            img_temp.write(response.read())
            img_temp.flush()

        artist.image.save(
            f'{artist.stage_name}_{artist.spotify_id}_{int(time.time())}.jpg',
            File(img_temp),
        )

        artist.save()
        last_popularity = artist.popularity_history.last()
        if not last_popularity or (
            last_popularity and (timezone.now() - last_popularity.created_at).days > 6
        ):
            monthly_listeners = private_client.get_artist_monthly_listeners(
                artist.spotify_id
            )
            score = ArtistPopularity.compute_parterre_score(
                data.get('popularity'),
                data.get('followers').get('total'),
                monthly_listeners,
            )
            pop = ArtistPopularity(
                spotify_popularity=data.get('popularity'),
                spotify_followers=data.get('followers').get('total'),
                monthly_listeners=monthly_listeners,
                parterre_score=score,
                artist=artist,
            )
            pop.save()


@shared_task
def import_top_tracks(artist_ids):
    for artist in Artist.objects.filter(id__in=artist_ids):
        data = client.get_artists_top_tracks(artist.spotify_id)
        for track_data in data.get('tracks'):
            track, _ = Track.objects.get_or_create(name=track_data.get('name'), spotify_id=track_data.get('id'))
            artist_spotify_names = [a.get('name') for a in track_data.get('artists')]
            artists = Artist.objects.filter(stage_name__in=artist_spotify_names)
            track.artists.add(*list(artists))

            last_popularity = track.popularity_history.last()
            if not last_popularity or (
                last_popularity
                and (timezone.now() - last_popularity.created_at).days > 6
            ):
                plays = private_client.get_track_play_count(track.spotify_id)
                pop = TrackPopularity(
                    spotify_popularity=track_data.get('popularity'),
                    spotify_plays=plays,
                    track=track,
                )
                pop.save()


@shared_task
def update_all_active_artists():
    artist_ids = Artist.objects.filter(
        deleted_at__isnull=True
    ).values_list('id', flat=True)

    import_artist_data(list(artist_ids))
    import_top_tracks(list(artist_ids))
