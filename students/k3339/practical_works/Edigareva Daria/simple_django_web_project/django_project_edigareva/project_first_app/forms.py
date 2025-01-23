import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Car, CarOwner


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['registration_number', 'make', 'model', 'color']


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(required=False)

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
        'first_name', 'last_name', 'email', 'username', 'passport_number', 'home_address',
        'nationality')  # + tuple(x.name for x in model._meta.fields)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            logging.getLogger(__name__).info(f"User {user.username} created (type: {type(user)})")
            owner = CarOwner(user=user, birth_date=self.cleaned_data['birth_date'])
            owner.save()
        return user
