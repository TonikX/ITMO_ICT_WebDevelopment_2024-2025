from .models import CarOwner, Car
from django import forms
from django.contrib.auth.models import User
from .models import CarOwner

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['last_name', 'first_name', 'birth_date']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'birth_date': 'Дата рождения',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color']


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['user', 'passport_number', 'address', 'nationality']
