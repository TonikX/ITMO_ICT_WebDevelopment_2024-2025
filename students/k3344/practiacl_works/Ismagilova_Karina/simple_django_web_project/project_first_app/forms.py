from django import forms
from .models import Owner, Car

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date', 'passport', 'address', 'nationality']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_brand', 'car_model', 'car_number', 'colour']