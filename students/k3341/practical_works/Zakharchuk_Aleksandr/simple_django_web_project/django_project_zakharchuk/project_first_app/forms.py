from django import forms

from project_first_app import models


class OwnerForm(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = [
            "username",
            "last_name",
            "first_name",
            "birth_date",
            "passport",
            "address",
            "nationality",
        ]


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = "__all__"
