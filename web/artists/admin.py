import csv

from django.contrib import admin, messages
from django.http import HttpResponse

from artists.models import Artist, Profile, ArtistPopularity, Track, Genre
from artists.tasks import import_artist_data, import_top_tracks
from spotify.clients import SpotifyAPI


class ArtistProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class ArtistPopularityInline(admin.TabularInline):
    model = ArtistPopularity
    can_delete = False
    extra = 0

    verbose_name_plural = "Popularity"

    readonly_fields = (
        "spotify_popularity",
        "spotify_followers",
        "monthly_listeners",
        "parterre_score",
    )


class TrackInline(admin.TabularInline):
    model = Track.artists.through
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]


class ArtistAdmin(admin.ModelAdmin):
    fields = ('spotify_url', 'stage_name', 'image', 'bio', 'force_visible', 'genres')
    inlines = [ArtistProfileInline, ArtistPopularityInline, TrackInline]
    actions = ['import_artist_data_from_spotify', 'import_top_tracks_from_spotify', "export_as_csv", "spotify_genre_list"]
    list_filter = ['stage_name', ]
    export_fields = ["id", "stage_name", "spotify_url", "genre_name_list"]

    def import_artist_data_from_spotify(self, request, queryset):
        import_artist_data.delay(list(queryset.values_list('id', flat=True)), notify_on_complete=True, user=request.user.username)
        self.message_user(
            request,
            f"The system will import spotify data for {queryset.count()} artists in the background",
            messages.SUCCESS,
        )

    def import_top_tracks_from_spotify(self, request, queryset):
        import_top_tracks.delay(list(queryset.values_list('id', flat=True)), notify_on_complete=True, user=request.user.username)
        self.message_user(
            request,
            f"The system will import the top tracks on spotify for {queryset.count()} artists in the background",
            messages.SUCCESS,
        )

    def export_as_csv(self, request, queryset):
        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(self.export_fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in self.export_fields])

        return response

    export_as_csv.short_description = "Esporta selezionati"

    def spotify_genre_list(self, request, queryset):
        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        client = SpotifyAPI()

        writer.writerow(['stage_name', 'spotify_genres'])
        for obj in queryset:
            artist_json = client.get_artist(obj.spotify_id)
            writer.writerow([obj.stage_name, ', '.join(artist_json['genres'])])

        return response

    spotify_genre_list.short_description = "Esporta generi da Spotify"

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre)
