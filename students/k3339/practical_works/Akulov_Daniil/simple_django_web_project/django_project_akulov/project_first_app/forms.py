from django import forms
from .models import Car, Owner

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "username",
            "password",
            "last_name",
            "first_name",
            "birth_date",
            "passport",
            "nationality",
            "address"
        ]

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'