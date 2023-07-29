from django.urls import path

from parterre.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
