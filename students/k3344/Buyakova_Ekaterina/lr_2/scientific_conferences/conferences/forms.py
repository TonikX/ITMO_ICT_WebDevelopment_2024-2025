from django import forms
from .models import Registration, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Форма для регистрации на конференцию
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['presentation_topic']

# Форма для написания отзыва о конференции
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }


# Форма для регистрации
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']