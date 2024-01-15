from django.urls import path

from explore.views import ExploreView, SearchView
from marketplace.views import MarketPlaceView

urlpatterns = [
    path("marketplace", MarketPlaceView.as_view(), name="marketplace"),
]
