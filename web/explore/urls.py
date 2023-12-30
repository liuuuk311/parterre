from django.urls import path

from explore.views import ExploreView, SearchView

urlpatterns = [
    path("explore", ExploreView.as_view(), name="explore"),
    path("explore/search", SearchView.as_view(), name="search"),
]
