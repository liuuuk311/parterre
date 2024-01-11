from django.contrib import admin, messages
from artists.models import Artist, Profile, ArtistPopularity, Track, Genre
from artists.tasks import import_artist_data, import_top_tracks


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
    actions = ['import_artist_data_from_spotify', 'import_top_tracks_from_spotify']
    list_filter = ['stage_name', ]

    def import_artist_data_from_spotify(self, request, queryset):
        import_artist_data.delay(list(queryset.values_list('id', flat=True)))
        self.message_user(
            request,
            f"The system will import spotify data for {queryset.count()} artists in the background",
            messages.SUCCESS,
        )

    def import_top_tracks_from_spotify(self, request, queryset):
        import_top_tracks.delay(list(queryset.values_list('id', flat=True)))
        self.message_user(
            request,
            f"The system will import the top tracks on spotify for {queryset.count()} artists in the background",
            messages.SUCCESS,
        )


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre)
