from django.contrib import admin, messages

from artists.models import Artist, Profile
from artists.tasks import import_artist_data, import_top_tracks


class ArtistProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class ArtistAdmin(admin.ModelAdmin):
    fields = ('spotify_url', 'stage_name', 'image', 'bio', 'force_visible')
    inlines = [ArtistProfileInline]
    actions = ['import_artist_data_from_spotify', 'import_top_tracks_from_spotify']

    def import_artist_data_from_spotify(self, request, queryset):
        import_artist_data(list(queryset.values_list('id', flat=True)))
        self.message_user(
            request,
            f"The system will import spotify data for {queryset.count()} artists",
            messages.SUCCESS,
        )

    def import_top_tracks_from_spotify(self, request, queryset):
        import_top_tracks(list(queryset.values_list('id', flat=True)))
        self.message_user(
            request,
            f"The system will import the top tracks on spotify for {queryset.count()} artists",
            messages.SUCCESS,
        )


admin.site.register(Artist, ArtistAdmin)
