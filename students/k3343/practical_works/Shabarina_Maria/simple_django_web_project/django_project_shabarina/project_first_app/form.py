from django import forms
from .models import CarOwner, Car


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ["first_name", "last_name", "date_of_birth", "passport", "address", "nationality"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["brand", "model", "color", "gos_number"]


class CarDeleteForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all(), label="Select Car to Delete")