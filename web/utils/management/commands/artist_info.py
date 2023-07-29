import csv
from urllib.parse import urlparse

from django.core.management.base import BaseCommand

from spotify.clients import SpotifyAPI, SpotifyPartnerAPI

client = SpotifyAPI()
private_client = SpotifyPartnerAPI()


class Command(BaseCommand):
    help = 'Process a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='CSV file to process')
        parser.add_argument('-o', '--output', type=str, help='Output file name')

    def handle(self, *args, **options):
        file_path = options['file']
        output = options['output'] or 'output.csv'

        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header

            new_rows = [
                ["Artist name", "URL", "Popularity", "Followers", "Monthly Listeners"]
            ]
            for row in csv_reader:
                if len(row) < 2 or not row[1]:
                    continue

                artist_id = self._url_to_spotify_id(row[1])
                artist_data = client.get_artist(artist_id)
                artist_monthly_listeners = private_client.get_artist_monthly_listeners(
                    artist_id
                )
                new_rows.append(
                    [
                        row[0],
                        row[1],
                        artist_data.get('popularity'),
                        artist_data.get('followers').get('total'),
                        artist_monthly_listeners,
                    ]
                )

        with open(output, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(new_rows)

        self.stdout.write(self.style.SUCCESS(f"Processed CSV. Output at {output}"))

    @staticmethod
    def _url_to_spotify_id(spotify_url):
        url = urlparse(spotify_url)
        return url.path.split('/')[-1]
