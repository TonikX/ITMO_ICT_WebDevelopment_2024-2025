from django import forms
from .models import Reservation, Review, Client
from django.contrib.auth.forms import UserCreationForm


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "client",
            "room",
            "check_in_date",
            "check_out_date"
        ]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Client
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "reservation",
            "comment",
            "rating"
        ]
