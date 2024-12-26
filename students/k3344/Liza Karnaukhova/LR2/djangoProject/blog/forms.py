from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from blog.models import Submission, Homework, User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role', 'student_class']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'assigned_date', 'due_date', 'description', 'penalties_info']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_text']


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date']
