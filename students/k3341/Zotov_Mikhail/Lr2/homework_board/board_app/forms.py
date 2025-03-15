from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, HomeworkSubmission, GradeHomework


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'role',
            'group',
        ]


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['solution_text']


class GradeHomeworkForm(forms.ModelForm):
    class Meta:
        model = GradeHomework
        fields = ['grade', 'penalty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].widget = forms.NumberInput(attrs={'min': 1, 'max': 10})
        self.fields['penalty'].widget = forms.NumberInput(attrs={'min': 0, 'max': 10})
