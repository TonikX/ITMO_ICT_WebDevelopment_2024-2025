from django import forms
from django.contrib.auth.models import User
from .models import Hotel, RoomType, Reservation, Review, Room


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'room']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError('End date should be after start date.')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['stay_period', 'comment', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 10:
            raise forms.ValidationError('Rating should be between 1 and 10.')
        return rating


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_number', 'room_type']
