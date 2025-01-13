from django import forms
from .models import Registration, Comment
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['team_name', 'car_description', 'racer_description', 'experience', 'class_level']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')