# Формы
Добавляю форму регистрации пользователя, форму для бронирования, форму для отзывов и форму для фильтрации туров. 

**код из файла forms.py:**
```python
from django import forms
from django.contrib.auth.models import User
from .models import Booking, Review

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

class BookingForm(forms.ModelForm):
    number_of_seats = forms.IntegerField(min_value=1, label="Number of Seats")

    class Meta:
        model = Booking
        fields = ['number_of_seats']

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ['text', 'rating']

class TourFilterForm(forms.Form):
    name = forms.CharField(required=False, label="Tour name", max_length=100)
    start_date = forms.DateField(required=False, label="Start date", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, label="End date", widget=forms.DateInput(attrs={'type': 'date'}))
```
