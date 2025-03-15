from django import forms
from . import models


class OwnerForm(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = [
            "last_name",
            "first_name",
            "birth_date",
        ]