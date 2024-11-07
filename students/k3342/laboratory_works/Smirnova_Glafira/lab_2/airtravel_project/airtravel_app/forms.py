from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Review, Reservation, Passenger, User


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment_text', 'rating']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        flight = kwargs.pop('flight', None)
        super(ReviewForm, self).__init__(*args, **kwargs)

        if user:
            self.instance.user = user

        if flight:
            self.instance.flight = flight


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        flight = kwargs.pop('flight', None)
        seat = kwargs.pop('seat', None)
        super(ReservationForm, self).__init__(*args, **kwargs)

        if user:
            self.instance.user = user

        if flight:
            self.instance.flight = flight

        if seat:
            self.instance.seat = seat


class EditReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(EditReservationForm, self).__init__(*args, **kwargs)


class RegisterPassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['ticket_number']

    def __init__(self, *args, **kwargs):
        super(RegisterPassengerForm, self).__init__(*args, **kwargs)


class TicketNumberForm(forms.Form):
    ticket_number = forms.CharField(max_length=20, label='Ticket Number')
