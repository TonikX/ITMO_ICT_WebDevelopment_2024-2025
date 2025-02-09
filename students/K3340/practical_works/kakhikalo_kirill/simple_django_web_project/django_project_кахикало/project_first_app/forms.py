from django import forms
from .models import AutoOwner


class AutoOwnerForm(forms.ModelForm):
    class Meta:
        model = AutoOwner

        fields = [
            "surname",
            "name",
            "date_of_birth"
        ]