from typing import Dict

import requests
from django.conf import settings


class SpotifyAPI:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.access_token = None

    def _get_auth_token(self):
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}",
        )
        data = response.json()
        self.access_token = data.get('access_token', None)

    def _make_get_request(self, url, params=None):
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.access_token}"}, params=params
        )

        if response.status_code == 401:
            self._get_auth_token()
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                params=params,
            )

        return response

    def get_artists_top_tracks(self, artist_id):
        response = self._make_get_request(
            f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
            params={"market": "IT"},
        )
        if response.status_code == 200:
            return response.json()

    def get_artist(self, artist_id):
        response = self._make_get_request(
            f"https://api.spotify.com/v1/artists/{artist_id}"
        )
        if response.status_code == 200:
            return response.json()

    def get_playlist(self, playlist_id):
        response = self._make_get_request(
            f"https://api.spotify.com/v1/playlists/{playlist_id}"
        )
        if response.status_code == 200:
            return response.json()


class SpotifyPartnerAPI:
    def __init__(self):
        self.client_version = settings.SPOTIFY_PARTNER_CLIENT_VERSION
        self.dc_cookie = settings.SPOTIFY_DC_COOKIE
        self.key_cookie = settings.SPOTIFY_KEY_COOKIE
        self.client_id = None
        self.access_token = None
        self.client_token = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

    def _get_client_token(self):
        if self.client_id is None:
            return

        data = {
            "client_data": {
                "client_version": self.client_version,
                "client_id": self.client_id,
                "js_sdk_data": {
                    "device_brand": "unknown",
                    "device_model": "desktop",
                    "os": "Linux",
                    "os_version": "unknown",
                },
            }
        }

        response = requests.post(
            "https://clienttoken.spotify.com/v1/clienttoken",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=data,
        )

        if response.status_code != 200:
            return

        json_response = response.json()
        self.client_token = json_response.get('granted_token', {}).get('token')

    def _get_access_token(self):
        if self.dc_cookie is None:
            return

        if self.key_cookie is None:
            return

        response = requests.get(
            "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
            headers={
                "user-agent": self.user_agent,
                "Cookie": f"sp_dc={self.dc_cookie};sp_key={self.key_cookie}",
            },
        )
        if response.status_code != 200:
            return

        data = response.json()
        self.access_token = data.get('accessToken')
        self.client_id = data.get('clientId')

    def _make_get_request(self, url, params):
        if not self.access_token:
            self._get_access_token()

        if not self.client_id or not self.client_token:
            self._get_client_token()

        headers = {
            'authority': 'api-partner.spotify.com',
            'accept': 'application/json',
            'accept-language': 'en',
            'app-platform': 'WebPlayer',
            'authorization': f'Bearer {self.access_token}',
            'client-token': f'{self.client_token}',
            'content-type': 'application/json;charset=UTF-8',
            'dnt': '1',
            'origin': 'https://open.spotify.com',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'spotify-app-version': '1.2.9.2093.geb8e5df4',
            'user-agent': self.user_agent,
        }
        return requests.get(url, headers=headers, params=params)

    def _make_query(self, params: Dict) -> Dict:
        response = self._make_get_request(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params
        )
        if response.status_code != 200:
            print(response.status_code)
            return

        return response.json()

    def get_track_play_count(self, track_id):
        data = self._make_query(
            {
                'operationName': 'getTrack',
                'variables': f'{{"uri":"spotify:track:{track_id}"}}',
                'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"6af75b996d93636e4f1980c170f1171a457bf936f47d6ee1e38f57671d3ae7bd"}}',
            }
        )
        if not data:
            print("No data")
            return
        try:
            return int(data['data']['trackUnion']['playcount'])
        except ValueError:
            print(data['data']['trackUnion']['playcount'])
            return

    def get_artist_monthly_listeners(self, artist_id):
        data = self._make_query(
            {
                'operationName': 'queryArtistOverview',
                'variables': f'{{"uri":"spotify:artist:{artist_id}","locale":""}}',
                'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"b82fd661d09d47afff0d0239b165e01c7b21926923064ecc7e63f0cde2b12f4e"}}',
            }
        )
        if not data:
            print("No data")
            return 0
        try:
            return int(data['data']['artistUnion']['stats']['monthlyListeners'])
        except ValueError:
            print(data)
            return 0
