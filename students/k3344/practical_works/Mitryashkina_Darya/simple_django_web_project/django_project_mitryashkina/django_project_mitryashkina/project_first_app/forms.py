from django import forms
from .models import User, Car
  
  
class UserForm(forms.ModelForm):
  
    class Meta:
        model = User
  
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'passport',
            'nationality',
            'address'
        ]

class CarForm(forms.ModelForm):

    class Meta:
        model = Car

        fields = [
            'state_number',
            'brand',
            'model',
            'color'
        ]