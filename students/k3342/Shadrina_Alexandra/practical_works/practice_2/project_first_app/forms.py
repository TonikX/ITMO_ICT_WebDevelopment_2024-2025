from django import forms
from .models import CarOwner, Car


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['last_name', 'first_name', 'birth_date', 'passport_number', 'nationality', 'home_address']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_model', 'car_brand', 'gov_number', 'car_color']

