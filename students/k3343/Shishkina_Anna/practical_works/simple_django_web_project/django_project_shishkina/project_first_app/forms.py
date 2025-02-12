from django import forms
from .models import Owner, Car, CustomUser
from django.contrib.auth.forms import UserCreationForm

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['last_name', 'first_name', 'date_of_birth']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_number', 'brand', 'car_model', 'colour']
        

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'passport_number', 'home_address', 'nationality')
