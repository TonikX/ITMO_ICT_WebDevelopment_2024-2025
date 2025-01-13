from django import forms
from .models import Owner, Car


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'email',
            'nationality',

        ]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'state_num',
            'brand',
            'model',
            'color'
        ]
