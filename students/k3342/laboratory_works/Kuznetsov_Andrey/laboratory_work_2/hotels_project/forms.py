from django import forms
from .models import Reservation, Review


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "user",
            "room",
            "check_in_date",
            "check_out_date"
        ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "reservation",
            "comment",
            "rating"
        ]
