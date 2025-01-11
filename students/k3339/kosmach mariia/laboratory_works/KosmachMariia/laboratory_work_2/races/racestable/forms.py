from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from racestable.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name"]


class RacerForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ["team", "car", "description", "experience", "type"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_type", "rating", "text"]


class RaceConnectionForm(forms.ModelForm):
    class Meta:
        model = RaceConnection
        fields = ["race"]
