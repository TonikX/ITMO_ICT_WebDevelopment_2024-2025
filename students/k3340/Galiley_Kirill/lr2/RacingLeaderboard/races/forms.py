from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Driver, Car, Comment, Registration, RaceResult

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')
    bio = forms.CharField(widget=forms.Textarea, required=False, label='О себе')
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'bio', 'avatar', 'password1', 'password2')

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('team', 'experience', 'driver_class', 'description')

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'comment_type', 'rating')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []

class RaceResultForm(forms.ModelForm):
    class Meta:
        model = RaceResult
        fields = ('position', 'time', 'points')
