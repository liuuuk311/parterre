from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from utils.views import AppContextMixin


# Create your views here.
class MarketPlaceView(LoginRequiredMixin, AppContextMixin, TemplateView):
    template_name = "marketplace/index.html"
