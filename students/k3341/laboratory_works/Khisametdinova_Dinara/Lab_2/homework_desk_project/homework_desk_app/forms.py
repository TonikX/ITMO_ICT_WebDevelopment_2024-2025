from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'role']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Хэширование
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class SubjectForm(forms.ModelForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='teacher'),
        widget=forms.CheckboxSelectMultiple,
        label='Преподаватели'
    )

    class Meta:
        model = Subject
        fields = ['name', 'description', 'teachers']

class GradeSubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['grade']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_text']
        widgets = {
            'submitted_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите ваше решение здесь...'
            }),
        }
        labels = {
            'submitted_text': 'Решение',
        }

class HomeworkCreateForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'issued_date', 'due_period', 'description', 'penalties_info']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'penalties_info': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teachers=user)

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade']