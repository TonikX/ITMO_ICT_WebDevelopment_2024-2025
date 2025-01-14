# forms.py
from django import forms
from .models import CustomUser, Car


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'passport_number', 'home_address', 'nationality')
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'passport_number', 'home_address', 'nationality')


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('license_plate', 'make', 'model', 'color')


