from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Booking, Review, Agency, Tour

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class TravelAgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'contact_info']

class TourForm(forms.ModelForm):
    price = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d+(\.\d{1,2})?$', 'Enter a valid price.')],
        widget=forms.TextInput(attrs={'pattern': '[0-9]*', 'title': 'Enter numbers only'})
    )

    class Meta:
        model = Tour
        fields = ['name', 'country', 'description', 'start_date', 'end_date', 'payment_terms', 'price']