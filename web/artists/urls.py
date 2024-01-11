from django.urls import path

from artists.views import ArtistDetailView, BuyArtistView, SellArtistView

urlpatterns = [
    path("artist/<uuid:pk>", ArtistDetailView.as_view(), name="artist-detail"),
    path("artist/<uuid:pk>/buy", BuyArtistView.as_view(), name="buy-artist"),
    path("artist/<uuid:pk>/sell", SellArtistView.as_view(), name="sell-artist"),
]
