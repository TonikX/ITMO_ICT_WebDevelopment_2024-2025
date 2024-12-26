from django import forms
from project_first_app.models import *


class CreateOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "username", "password", "first_name",
            "last_name", "birth_date", "passport",
            "address", "nationality"
        ]
        labels = {
            "username": "Username",
            "password": "Password",
            "first_name": "Name",
            "last_name": "Surname",
            "birth_date": "Birth date",
            "passport": "Passport",
            "address": "Address",
            "nationality": "nationality"
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
