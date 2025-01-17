from django import forms
from .models import User, Car
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name', 'birth_date', 'passport_number', 'address', 'nationality'
        ]

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['registration_number', 'brand', 'model', 'color']