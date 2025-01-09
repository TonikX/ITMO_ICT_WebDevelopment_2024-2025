from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Homework, Submission


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date')  # Только редактируемые поля


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'assigned_date', 'due_date', 'description', 'penalties']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_text']


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade']
