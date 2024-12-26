from django import forms
from project_first_app.models import *


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "username", "password", "first_name", "last_name", "birth_date", "passport_number", "home_address", "nationality"
        ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["license_plate", "brand", "model", "color"]
