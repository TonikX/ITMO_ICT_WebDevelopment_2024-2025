from django import forms
from .models import User, Grade, Class, Task, Discipline
from django.contrib.auth.forms import UserCreationForm


class SchoolUserCreationForm(UserCreationForm):
    class_field = forms.ModelChoiceField(queryset=Class.objects.all(), required=True, label="Класс", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['answer']


class TeachersSubmissionForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['number']


class TeachersCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'issue_date', 'due_date', 'discipline_id', 'class_id']

    discipline_id = forms.ModelChoiceField(queryset=Discipline.objects.all(), empty_label="Выберите дисциплину")
    class_id = forms.ModelChoiceField(queryset=Class.objects.all(), empty_label="Выберите класс")
    issue_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Выберите", "месяц", "год")))
    due_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Выберите", "месяц", "год")))
