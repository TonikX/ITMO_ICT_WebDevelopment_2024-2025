from django import forms

from .models import CarOwner, Car


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "passport_data",
            "address",
            "nationality",
        ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "number",
            "brand",
            "model",
            "color",
        ]
