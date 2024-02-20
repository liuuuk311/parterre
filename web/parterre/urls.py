from django.urls import path

from parterre.views import HomeView, CreateContactView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("/contact", CreateContactView.as_view(), name="contact"),
]
