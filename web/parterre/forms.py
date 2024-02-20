from django import forms

from parterre.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['name', 'email', 'message']
        model = Contact