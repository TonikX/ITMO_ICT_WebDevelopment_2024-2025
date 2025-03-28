from django import forms
from .models import Submission
from django.contrib.auth.forms import AuthenticationForm

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['text_submission']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
