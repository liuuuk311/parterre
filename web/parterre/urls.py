from django.urls import path

from parterre.views import HomeView, CreateContactView, SuccessContactView, ContactView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("/contact", CreateContactView.as_view(), name="contact"),
    path("/feeback", ContactView.as_view(), name="app_feedback"),
    path("/success", SuccessContactView.as_view(), name="contact-success"),
]
