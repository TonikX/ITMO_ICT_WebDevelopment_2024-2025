from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation, Review


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = {'room', 'start_date', 'end_date'}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = {'reservation', 'review', 'rate'}
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
