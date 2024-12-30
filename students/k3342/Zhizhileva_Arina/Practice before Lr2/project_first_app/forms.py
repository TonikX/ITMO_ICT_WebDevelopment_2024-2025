from django import forms
from .models import Owner, Auto

class CarOwnerForm(forms.ModelForm):
   class Meta:
       model = Owner
       fields = ['first_name', 'last_name', 'date_of_birth', 'cars', 'passport_number', 'home_address', 'nationality', 'password', 'username']

class CarForm(forms.ModelForm):
   class Meta:
       model = Auto
       fields = ['model', 'type_of_car', 'gov_number', 'color']
