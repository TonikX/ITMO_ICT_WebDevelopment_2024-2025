from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AuthorRegistration, Review

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = AuthorRegistration
        fields = ['presentation_title']  # можно добавить другие поля, если потребуется

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment_text', 'rating']