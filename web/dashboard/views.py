from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from artists.models import Artist
from utils.views import AppContextMixin


class DashboardView(LoginRequiredMixin, AppContextMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.has_label:
            return redirect('create_label')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.filter(stage_name__isnull=False).all()
        return context
