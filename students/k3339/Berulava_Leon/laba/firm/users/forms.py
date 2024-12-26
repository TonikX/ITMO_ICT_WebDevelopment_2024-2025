from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите имя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-group',
        'placeholder': 'email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group',
        'placeholder': 'Введите пароль еще раз'
    }))
    is_agent = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Вы турагент?")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_agent')
