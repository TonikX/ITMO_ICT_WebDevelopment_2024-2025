from django import forms
from . import models

class OwnerForm(forms.ModelForm):

    class Meta:
        model = models.CarOwner
        fields = ["first_name", "last_name", "birth_date"]

class UserForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ["username", "password", "passport_number", "address", "nationality"]

