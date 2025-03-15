from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Owner, Car


class OwnerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Owner
        fields = ('first_name', 'last_name') + UserCreationForm.Meta.fields + ('passport_number', 'home_address', 'nationality')


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'state_number', 'color']
