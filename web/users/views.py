from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, UserRegisterForm, UserLabelForm


class CustomLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class CreateRecordLabelView(CreateView):
    template_name = 'label/create_your_label.html'
    success_url = reverse_lazy('welcome')
    form_class = UserLabelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RecordLabelInfoView(TemplateView):
    template_name = 'label/label_info.html'
