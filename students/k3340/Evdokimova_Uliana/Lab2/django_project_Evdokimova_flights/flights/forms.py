from django import forms
from .models import Reservation, Review

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['flight', 'seat_number']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['flight', 'text', 'rating']
