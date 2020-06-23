from django import forms
from service.models import Service


class ServiceForm(forms.ModelForm):

    class Meta:

        model = Service
        fields = ('user', 'person', 'title', 'category', 'description', 'direction', 'facebook_url', 'picture_logo')