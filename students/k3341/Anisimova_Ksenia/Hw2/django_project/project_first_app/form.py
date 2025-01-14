from django import forms
from .models import carOwner


class OwnerForm(forms.ModelForm):
    class Meta:
        model = carOwner
        fields = [
            "surname",
            "name",
            "date_Birth"
        ]
