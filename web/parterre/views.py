from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class WebsiteContextMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [
            {'label': _('home'), 'url': ''},
            {'label': _('how it works'), 'url': ''},
        ]
        return context


class HomeView(WebsiteContextMixin):
    template_name = "parterre/home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)
