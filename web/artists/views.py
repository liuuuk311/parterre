from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import DetailView, CreateView
from django.views.generic.base import TemplateResponseMixin

from artists.models import Artist
from utils.helpers import create_svg_chart
from utils.views import AppContextMixin


class ArtistDetailView(DetailView, AppContextMixin):
    model = Artist
    template_name = 'artists/artist_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['full_stars'] = range(0)
        context['empty_stars'] = range(5)
        context['svg_chart'] = create_svg_chart(
            [
                p.spotify_popularity
                for p in kwargs.get('object').popularity_history.order_by(
                    "-created_at"
                )[:5:-1]
            ]
        )
        return context


class BuyArtistView(View, TemplateResponseMixin, AppContextMixin):
    def post(self, request, *args, **kwargs):
        artist = Artist.objects.filter(id=kwargs.get('pk')).first()
        if not artist:
            return Http404()

        success = self.request.user.buy_artist(artist)
        if not success:
            self.template_name = "artists/partials/artist_purchase_failed.html"
            return self.render_to_response(super().get_context_data())

        self.template_name = "artists/partials/artist_bought.html"
        return self.render_to_response(super().get_context_data())


class SellArtistView(View, TemplateResponseMixin, AppContextMixin):
    def post(self, request, *args, **kwargs):
        artist = Artist.objects.filter(id=kwargs.get('pk')).first()
        if not artist:
            return Http404()

        success = self.request.user.sell_artist(artist)
        if not success:
            self.template_name = "artists/partials/artist_purchase_failed.html"
            return self.render_to_response(super().get_context_data())

        self.template_name = "artists/partials/artist_bought.html"
        return self.render_to_response(super().get_context_data())
