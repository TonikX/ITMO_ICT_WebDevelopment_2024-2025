from django import forms
from .models import Car, Owner

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['gos_number', 'brand', 'car_model', 'color']

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }