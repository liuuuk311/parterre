from crispy_forms.helper import FormHelper
from django.forms import BaseInlineFormSet


class ExcludeMarkedAsDeletedInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.only_active()


class BaseInlineFormSetWithHelper(ExcludeMarkedAsDeletedInlineFormset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = "justify-self-stretch mb-3"
