from django import forms
from .models import Car, User 
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'passport_number', 'home_address', 'nationality', 'birth_date',
                 'password1', 'password2')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
            'birth_date': 'Дата рождения',
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'brand', 'model', 'color']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'А123ВС77'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Toyota'}),
            'model': forms.TextInput(attrs={'placeholder': 'Camry'}),
            'color': forms.TextInput(attrs={'placeholder': 'Черный'}),
        }
        labels = {
            'number': 'Гос номер',
            'brand': 'Марка',
            'model': 'Модель', 
            'color': 'Цвет',
        }


