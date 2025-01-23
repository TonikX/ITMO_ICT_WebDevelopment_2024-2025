from django import forms
from .models import Car_owner, Car

class OwnerForm(forms.ModelForm):
    
    class Meta:
        model = Car_owner

        fields = ['last_name', 'first_name', 'birth_date', 'passport_number', 'address', 'nationality']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['state_number', 'brand', 'model', 'color']
