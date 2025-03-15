from django import forms
from .models import Owner, Car

class OwnerForm(forms.ModelForm):
     class Meta:
         model = Owner
         fields = ('last_name', 'first_name', 'birth_date', 'passport_number', 'home_address', 'nationality')

class CarForm(forms.ModelForm):
     class Meta:
         model = Car
         fields = '__all__'