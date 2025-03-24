from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HomeworkSubmission


class UserRegistrationForm(UserCreationForm):
    role_choices = [
        ('учитель', 'Учитель'),
        ('ученик', 'Ученик'),
    ]
    role = forms.ChoiceField(choices=role_choices)
    first_name = forms.CharField(max_length=100, label='Имя Отчество')
    last_name = forms.CharField(max_length=100, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role']


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['text_submission']  # Поле, в котором ученик будет писать свой ответ
        widgets = {
            'text_submission': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}),
        }
