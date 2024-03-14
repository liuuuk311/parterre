from django.urls import path

from parterre.views import HomeView, CreateContactView, SuccessContactView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("/contact", CreateContactView.as_view(), name="contact"),
    path("/success", SuccessContactView.as_view(), name="contact-success"),
]
