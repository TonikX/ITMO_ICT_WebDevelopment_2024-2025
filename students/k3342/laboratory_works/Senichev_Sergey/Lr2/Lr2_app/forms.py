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
        # Получаем пользователя из kwargs
        user = kwargs.pop('user', None)
        super(AssignmentForm, self).__init__(*args, **kwargs)

        if user:
            # Получаем все задания
            all_tasks = Task.objects.all()
            # Получаем задания, на которые студент уже отправил ответы
            submitted_tasks = Assignment.objects.filter(
                student__user=user
            ).values_list('task_id', flat=True)
            # Исключаем уже отправленные задания из списка
            available_tasks = all_tasks.exclude(id__in=submitted_tasks)

            # Обновляем queryset для поля task
            self.fields['task'].queryset = available_tasks
