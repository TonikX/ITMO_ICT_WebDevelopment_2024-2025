from django import forms
from django.contrib.auth import get_user_model

class LoginUserForm(forms.Form):
  username = forms.CharField(label='Login', widget=forms.TextInput())
  password = forms.CharField(label='Password', widget=forms.PasswordInput())

class RegisterUserForm(forms.ModelForm):
  username = forms.CharField(label='Login', widget=forms.TextInput())
  password = forms.CharField(label='Password', widget=forms.PasswordInput())
  password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())

  class Meta:
    model = get_user_model()
    fields = ['username', 'password']

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError("Passwords don't match")
    return cd['password']