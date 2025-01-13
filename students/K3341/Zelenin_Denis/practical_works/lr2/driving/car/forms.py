from django import  forms
from .models import Owner

class OwnerForm(forms.ModelForm):
    class Meta:

        model = Owner
        fields = [
            "name",
            "second_name",
            "birthdate",
            "nation",
            "username",
            "pasport_number",
            "password"

        ]