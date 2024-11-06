from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Hotel, Room, Booking, Review

class HotelCreateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            "name",
            "address",
            "description",
        ]

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'price', 'room_type', 'capacity', 'description']

class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
        ]

class BookingAdminCreateForm(forms.Form):
    room_number = forms.IntegerField(validators=[MinValueValidator(1)])
    username = forms.CharField(max_length=100)
    check_in = forms.DateTimeField()
    check_out = forms.DateTimeField()

    def getData(self):
        booking = {}
        booking['room_number'] = self.cleaned_data['room_number']
        booking['username'] = self.cleaned_data['username']
        booking['check_in'] = self.cleaned_data['check_in']
        booking['check_out'] = self.cleaned_data['check_out']
        return booking

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "rating",
            "text",
        ]