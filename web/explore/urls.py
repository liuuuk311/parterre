from django.urls import path

from explore.views import ExploreView, GenreView, SearchView

urlpatterns = [
    path("explore", ExploreView.as_view(), name="explore"),
    path("explore/search", SearchView.as_view(), name="search"),
    path("explore/genre/<str:genre>", GenreView.as_view(), name="genre")
]
