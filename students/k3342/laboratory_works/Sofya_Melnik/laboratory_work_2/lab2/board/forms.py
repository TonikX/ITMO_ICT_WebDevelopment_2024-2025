from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Homework, Submission

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role']


class UserLoginForm(AuthenticationForm):
    pass

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'assigned_date', 'due_date', 'description', 'penalties_info']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_text']


class GradeSubmissionForm(forms.ModelForm):
    grade = forms.IntegerField(min_value=0, max_value=5, required=False)

    class Meta:
        model = Submission
        fields = ['grade']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']