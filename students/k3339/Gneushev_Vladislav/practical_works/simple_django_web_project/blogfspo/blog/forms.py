from django import forms
from .models import CarOwner, Car


class CarOwnerForm(forms.ModelForm):
     class Meta:
         model = CarOwner
         fields = ('last_name', 'first_name', 'birth_date')


class CarForm(forms.ModelForm):
     class Meta:
         model = Car
         fields = '__all__'