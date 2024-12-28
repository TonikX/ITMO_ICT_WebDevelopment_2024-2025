from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import HotelBaseAccount
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    birth_date = forms.DateField(label="Birth Date", widget=forms.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))

    class Meta:
        model = HotelBaseAccount
        fields = ('firstname', 'lastname', 'email', 'birth_date')
        labels = {

        }

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_again')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords must match")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        accounts = HotelBaseAccount.objects.filter(email=email)
        if accounts.exists():
            raise ValidationError("Email already registered")
        return email

    def save(self, commit=True):
        account = super().save(commit=False)
        account.password = make_password(self.cleaned_data["password1"], hasher='pbkdf2_sha256')
        if commit:
            account.save()
        return account


class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = HotelBaseAccount
        fields = ('firstname', 'lastname', 'is_active')

    def clean_password(self):
        return self.initial["password1"]


class AdminCreationForm(forms.ModelForm):
    password = forms.CharField(label="Admin Password", widget=forms.PasswordInput)
    class Meta:
        model = HotelBaseAccount
        fields = ('firstname', 'lastname', 'email')
        labels = {
            "firstname": 'Admin name',
            "lastname": 'Admin surname',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        accounts = HotelBaseAccount.objects.filter(email=email)
        if accounts.exists():
            raise ValidationError("Email already by other administrator")
        return email

    def save(self, commit=True):
        account = super().save(commit=False)
        account.password = make_password(self.cleaned_data["password"], hasher='pbkdf2_sha256')
        account.is_staff = True
        admins_group = Group.objects.filter(name='Admins Group').first()
        account.groups.add(admins_group)
        if commit:
            account.save()
        return account


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput)