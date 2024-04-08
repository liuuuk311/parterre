from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from parterre.forms import ContactForm
from parterre.models import Contact


class WebsiteContextMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [
            {'label': _('home'), 'url': ''},
            {'label': _('Come funziona'), 'url': '#how-it-works'},
            {'label': _('Contattaci'), 'url': '#contact'},
        ]
        return context


class HomeView(WebsiteContextMixin):
    template_name = "parterre/home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            kwargs['form'] = ContactForm()
        
        return super().get_context_data(**kwargs)


class CreateContactView(SuccessMessageMixin, CreateView):
    success_message = "Your message was sent successfully"
    model = Contact
    form_class = ContactForm
    template_name = "parterre/home.html"
    success_url = reverse_lazy('contact-success')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactView(WebsiteContextMixin, TemplateView):
    template_name = "parterre/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SuccessContactView(WebsiteContextMixin, TemplateView):
    template_name = "parterre/success_contact.html"
