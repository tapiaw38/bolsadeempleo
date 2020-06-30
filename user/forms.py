from django import forms

class PersonForm(forms.Form):
    phone_number = forms.CharField(max_length=10, required=True)
    direction = forms.CharField(max_length=100, required=True)
    picture = forms.ImageField()

