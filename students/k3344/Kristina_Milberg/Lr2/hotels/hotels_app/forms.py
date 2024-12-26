from django import forms
from .models import Guest
from .models import Room
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'passport_number', 'home_address', 'nationality']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'capacity', 'amenities', 'price']  # Поля, которые нужно заполнить

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['user', 'phone_number']  # Поля, которые нужно заполнить
