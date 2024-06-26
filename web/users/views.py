from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from utils.views import AppContextMixin

from .forms import LoginForm, UserRegisterForm, UserLabelForm
from .models import Wallet


class CustomLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Profilo creato correttamente 👍"


class CreateRecordLabelView(LoginRequiredMixin, CreateView):
    template_name = 'label/create_your_label.html'
    success_url = reverse_lazy('welcome')
    form_class = UserLabelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RecordLabelInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'label/welcome.html'


class UserProfileView(AppContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'
