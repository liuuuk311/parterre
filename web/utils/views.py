from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, ListView
from django.views.generic.base import ContextMixin


class MarkAsDeletedActionView(ListView, DeleteView):
    object = None
    object_list = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_as_deleted()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class MarkAsDeletedView(DeleteView):
    object = None
    object_list = None

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.mark_as_deleted()
        return HttpResponseRedirect(success_url)


class AppContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [
            {'label': _('dashboard'), 'url': reverse_lazy('dashboard')},
            {'label': _('explore'), 'url': reverse_lazy('explore')},
        ]
        return context
