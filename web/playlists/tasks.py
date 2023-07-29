from celery import shared_task

from artists.models import Track
from playlists.models import Playlist
from spotify.clients import SpotifyAPI, SpotifyPartnerAPI

client = SpotifyAPI()
private_client = SpotifyPartnerAPI()


@shared_task
def import_playlist_data(playlist_ids):
    for playlist in Playlist.objects.filter(id__in=playlist_ids):
        data = client.get_playlist(playlist.spotify_id)
        playlist.name = data['name']
        playlist.followers = data['followers']['total']

        playlist.save()

        playlist.tracks.clear()

        for item in data['tracks']['items']:
            track = Track.objects.filter(spotify_id=item['track']['id']).first()
            if not track:
                continue

            playlist.tracks.add(track)
