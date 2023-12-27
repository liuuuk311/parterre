from django.contrib import admin

from playlists.models import Playlist
from playlists.tasks import import_playlist_data


class PlaylistAdmin(admin.ModelAdmin):
    fields = ('spotify_url',)
    actions = ['import_playlist_data']

    def import_playlist_data(self, request, queryset):
        import_playlist_data.delay(list(queryset.values_list('id', flat=True)))
        self.message_user(
            request,
            f"The system will check which tracks spotify data for {queryset.count()} artists in the background",
        )


admin.site.register(Playlist, PlaylistAdmin)
