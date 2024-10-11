from django import forms
from driving.models import Car, CarOwner
from django.contrib.auth import get_user_model


class CarOwnerForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput,
        required=True,
    )

    passport_number = forms.CharField(
        widget=forms.TextInput,
        required=True,
        min_length=6,
        max_length=6,
    )

    nationality = forms.CharField(
        widget=forms.TextInput,
        required=True,
        max_length=30,
    )

    home_address = forms.CharField(
        widget=forms.TextInput,
        required=True,
        max_length=50,
    )

    class Meta:
        model = CarOwner
        fields = (
            "last_name",
            "first_name",
            "birthdate",
            "email",
            "passport_number",
            "nationality",
            "home_address",
        )

    def clean_passport_number(self):
        passport_number: str = self.cleaned_data["passport_number"]
        if not passport_number.isdigit():
            raise forms.ValidationError("Номер паспорта должен содержать только цифры")

        if get_user_model().objects.filter(passport_number=passport_number).exists():
            raise forms.ValidationError(
                f"Водитель с номером паспорта {passport_number} уже существует"
            )

        return passport_number

    def clean_email(self):
        email: str = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email занят, укажите другой")

        return email


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = (
            "state_number",
            "brand",
            "model",
            "color",
        )
