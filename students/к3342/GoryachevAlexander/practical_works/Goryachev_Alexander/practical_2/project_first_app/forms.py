from django import forms
from .models import *


class CreateOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = [
            "name",
            "surname",
            "birthday_date",
        ]
        labels = {
            "name": "Name",
            "surname": "Surname",
            "birthday_date": "Birth date",
        }


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "state_number",
            "mark",
            "model",
            "colour"
        ]
        labels = {
            "state_number": "State Number",
            "mark": "Mark",
            "model": "Model",
            "colour": "Colour",
        }


class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "state_number",
            "mark",
            "model",
            "colour"
        ]
        labels = {
            "state_number": "State Number",
            "mark": "Mark",
            "model": "Model",
            "colour": "Colour",
        }


class DeleteCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "state_number",
            "mark",
            "model",
            "colour"
        ]
        labels = {
            "state_number": "State Number",
            "mark": "Mark",
            "model": "Model",
            "colour": "Colour",
        }
