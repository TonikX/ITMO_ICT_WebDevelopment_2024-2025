from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('room', 'check_in', 'check_out')
        widgets = {
        'check_in': forms.DateInput(attrs={'type': 'date'}),
        'check_out': forms.DateInput(attrs={'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('room', 'stay_from', 'stay_to', 'rating', 'text')
        widgets = {
        'stay_from': forms.DateInput(attrs={'type': 'date'}),
        'stay_to': forms.DateInput(attrs={'type': 'date'}),
        'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        'text': forms.Textarea(attrs={'rows': 4}),
        }