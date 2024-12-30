from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assignment, Task


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['task', 'text']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AssignmentForm, self).__init__(*args, **kwargs)

        if user:
            all_tasks = Task.objects.all()
            submitted_tasks = Assignment.objects.filter(
                student__user=user
            ).values_list('task_id', flat=True)
            available_tasks = all_tasks.exclude(id__in=submitted_tasks)

            self.fields['task'].queryset = available_tasks
