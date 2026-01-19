from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CarOwnerUser, Car

class CarOwnerUserCreationForm(UserCreationForm):
    class Meta:
        model = CarOwnerUser
        fields = [
            'username', 'password1', 'password2',
            'first_name', 'last_name', 'email',
            'passport', 'address', 'nationality', 'birth_date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport': 'Паспорт',
            'address': 'Адрес',
            'nationality': 'Национальность',
        }

class CarOwnerUserUpdateForm(UserChangeForm):
    class Meta:
        model = CarOwnerUser
        fields = [
            'first_name', 'last_name', 'email',
            'passport', 'address', 'nationality', 'birth_date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport': 'Паспорт',
            'address': 'Адрес',
            'nationality': 'Национальность',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'color', 'plate_number']
        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'color': 'Цвет',
            'plate_number': 'Госномер',
        }