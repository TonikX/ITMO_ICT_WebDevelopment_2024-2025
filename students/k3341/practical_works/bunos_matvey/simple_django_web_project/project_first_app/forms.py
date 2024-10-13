from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'color', 'state_number']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('passport_number', 'home_address', 'nationality')
