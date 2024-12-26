from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation, Review, Tour
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'date_of_birth']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = []


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)])
        }
