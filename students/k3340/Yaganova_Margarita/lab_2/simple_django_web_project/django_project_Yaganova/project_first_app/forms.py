from django import forms
from .models import *


class OwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['last_name', 'first_name', 'date_of_birth',
                  'passport_number', 'address', 'nationality', 'email',
                  'password']
