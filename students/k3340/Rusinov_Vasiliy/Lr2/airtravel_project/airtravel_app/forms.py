from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Review, Reservation, Passenger, User


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User  # Make sure to import your User model
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
        fields = ['comment_text', 'rating']  # Exclude user and flight fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        flight = kwargs.pop('flight', None)  # Get the flight from kwargs
        super(ReviewForm, self).__init__(*args, **kwargs)

        if user:
            self.instance.user = user  # Set the user instance
            # self.fields['user'].initial = f"{user.first_name} {user.last_name}" if hasattr(user, 'first_name') else
            # ""  # Autofill names (not stored in DB)

        if flight:
            self.instance.flight = flight  # Set the flight instance


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name']  # Exclude user, flight, and seat fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        flight = kwargs.pop('flight', None)  # Get the flight from kwargs
        seat = kwargs.pop('seat', None)  # Get the seat from kwargs
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

