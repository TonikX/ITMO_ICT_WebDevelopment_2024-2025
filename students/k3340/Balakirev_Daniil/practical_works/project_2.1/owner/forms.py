from django import forms
from .models import CarOwner, Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_number', 'mark', 'model', 'colour']

class CarOwnerCreateForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ["username", "password", "first_name", "last_name", "date_of_birthday", "passport", "home_address", "nationality"]