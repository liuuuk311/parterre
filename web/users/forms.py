from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from users.models import RecordLabel


class LoginForm(AuthenticationForm):
    username = EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive. "
            "If this is your first time to login, make sure to check your email and verify your email address"
        ),
        "inactive": _("This account is inactive."),
    }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name']


class UserLabelForm(forms.ModelForm):
    class Meta:
        model = RecordLabel
        fields = ['name']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.user_id:
            self.instance.user_id = user.id
