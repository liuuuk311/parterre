from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from artists.models import Artist, Genre
from explore.forms import ExploreSearchForm
from utils.views import AppContextMixin


class ExploreView(LoginRequiredMixin, AppContextMixin, TemplateView):
    template_name = "explore/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ExploreSearchForm()
        context['genres'] = Genre.objects.all()
        return context


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "explore/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.filter(
            stage_name__icontains=self.request.GET.get('search')
        )
        return context


class GenreView(LoginRequiredMixin, TemplateView):
    template_name = "explore/genre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.filter(
            genres__name=self.kwargs['genre']
        ).order_by('stage_name')
        context['genre'] = self.kwargs['genre']
        return context