from django import forms
from .models import Owner, Car

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date', 'Nationality', 'Address', 'Passport', 'password']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'state_number', 'colour']