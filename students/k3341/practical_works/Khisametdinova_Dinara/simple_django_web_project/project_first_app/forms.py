from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Car, CarOwner

class CreateOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "passport_number",
            "home_address",
            "nationality"
        ]
        labels = {
            "first_name": "Name",
            "last_name": "Surname",
            "birth_date": "Birth date",
            "passport_number": "Passport Number",
            "home_address": "Address",
            "nationality": "Nationality"
        }


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["number", "brand", "model", "color"]
        labels = {
            "number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }


class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["number", "brand", "model", "color"]
        labels = {
            "number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }