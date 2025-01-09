from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, DateField

from hotel_list.models import Reservation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReservationForm(ModelForm):
    dt_start = DateField(
        widget=DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Start Date'
        }),
        label='Start Date',
        required=True
    )
    dt_end = DateField(
        widget=DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'End Date'
        }),
        label='End Date',
        required=True
    )

    class Meta:
        model = Reservation
        fields = ['dt_start', 'dt_end']
