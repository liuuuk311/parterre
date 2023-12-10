from celery import shared_task

from artists.models import Artist
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
            artist_url = f"https://open.spotify.com/artist/{item['track']['artists'][0]['id']}"
            artist, _ = Artist.objects.get_or_create(spotify_url=artist_url)
            artist.save()
