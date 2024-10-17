from django import forms

from .models import Owner, Car


class OwnerCreateForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            'name',
            'surname',
            'birth_date',
        ]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'license_plate',
            'brand',
            'model',
            'color',
        ]
