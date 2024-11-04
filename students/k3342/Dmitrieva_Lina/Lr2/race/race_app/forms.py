from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Racer, User


class RacerForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['full_name', 'experience']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'passport_number', 'home_address', 'nationality', 'password1', 'password2']