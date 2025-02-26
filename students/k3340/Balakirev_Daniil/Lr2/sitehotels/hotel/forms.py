from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Booking, Review

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username',)

class BookingForm(forms.ModelForm):
    class Meta:
         model = Booking
         fields = ('check_in_date', 'check_out_date')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rating', 'start_date', 'end_date')

