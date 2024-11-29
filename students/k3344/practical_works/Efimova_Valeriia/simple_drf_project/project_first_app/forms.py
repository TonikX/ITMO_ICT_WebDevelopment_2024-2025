from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarOwner, Car, CustomUser


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ["first_name", "last_name", "birth_date"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["registration_number", "brand", "model", "color"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "passport_number",
            "home_address",
            "nationality",
        )