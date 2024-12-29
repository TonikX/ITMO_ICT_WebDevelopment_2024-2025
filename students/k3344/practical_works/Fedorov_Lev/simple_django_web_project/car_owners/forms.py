from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Owner, Car, License, Ownership, CustomUser


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'passport_number', 'home_address', 'nationality']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = '__all__'


class OwnershipForm(forms.ModelForm):
    class Meta:
        model = Ownership
        fields = '__all__'
