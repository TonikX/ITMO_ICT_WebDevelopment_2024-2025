from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Owner, Car, User


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'passport_number', 'home_address', 'nationality')

