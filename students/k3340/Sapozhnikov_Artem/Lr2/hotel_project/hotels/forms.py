from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Review

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('check_in', 'check_out')
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = self.initial.get('room')  # передадим вьюшкой (см. ниже)

        # Проверка, что даты корректны
        if check_in and check_out and check_in >= check_out:
            raise ValidationError('Дата заезда должна быть раньше даты выезда.')

        # Проверка пересечения дат
        if room and check_in and check_out:
            overlaps = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
                status__in=['reserved', 'checked_in']
            ).exists()
            if overlaps:
                raise ValidationError('Комната уже забронирована на эти даты.')

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('stay_from', 'stay_to', 'rating', 'text')
        widgets = {
            'stay_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stay_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Напишите ваш отзыв...'}),
        }