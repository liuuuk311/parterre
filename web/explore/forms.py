from crispy_forms.helper import FormHelper
from django import forms
from django.utils.translation import gettext_lazy as _


class ExploreSearchForm(forms.Form):
    search = forms.CharField(
        label="Search",
        strip=True,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search for artists..."),
                "type": "search",
                "hx-get": "/explore/search",
                "hx-trigger": "keyup[target.value.length > 3] changed, search, delay:300ms",
                "hx-target": "#search-results",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
