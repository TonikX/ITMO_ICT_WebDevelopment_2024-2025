from django import forms
from .models import *


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "last_name",
            "first_name",
            "birth_date",
            "passport_number",
            "nationality",
            "address"
        ]


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["state_number", "brand", "model", "color"]
        labels = {
            "state_number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }


class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["state_number", "brand", "model", "color"]
        labels = {
            "state_number": "Number",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
        }
