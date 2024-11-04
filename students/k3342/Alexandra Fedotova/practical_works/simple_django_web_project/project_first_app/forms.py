from django import forms
from .models import CarOwner, Car, CustomUser

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['first_name', 'last_name', 'date_of_birth']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['registration_number', 'make', 'model', 'color']

# Форма для создания пользователя
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['passport_number', 'home_address', 'nationality'] 
