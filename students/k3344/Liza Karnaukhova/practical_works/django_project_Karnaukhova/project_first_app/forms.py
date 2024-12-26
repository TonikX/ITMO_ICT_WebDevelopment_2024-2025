from django import forms

from project_first_app.models import Owner, Car


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = [
            "last_name",
            "first_name",
            "birth_date",
            "passport_number",
            "nationality",
            "home_address"
        ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
