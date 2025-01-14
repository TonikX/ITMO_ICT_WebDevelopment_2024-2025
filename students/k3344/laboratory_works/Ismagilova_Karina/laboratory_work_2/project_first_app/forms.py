from django import forms
from .models import Review, Participant, User, Results
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        labels = {
            'comment': 'Комментарий',
            'rating': 'Оценка',
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'age', 'email']
        labels = {
            'username': 'Никнейм',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
            'age': 'Полных лет',
            'email': 'Email'
        }

class AuthentificationCustomForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']

class ResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = ['accepted']
