from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RacingUser, Racer, RaceRegistration, Comment, Car


class RacingUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = RacingUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class RacingUserUpdateForm(UserChangeForm):
    class Meta:
        model = RacingUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience_years', 'phone', 'date_of_birth']


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team', 'racer_class', 'license_number']
        widgets = {
            'license_number': forms.TextInput(attrs={'placeholder': 'Введите номер лицензии'}),
        }


class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceRegistration
        fields = ['car']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'racer'):
            self.fields['car'].queryset = Car.objects.filter(team=user.racer.team)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите ваш комментарий...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }


class RaceSearchForm(forms.Form):
    # Используем жестко заданные choices вместо обращения к модели
    RACE_TYPE_CHOICES = [
        ('', 'Все типы'),
        ('Qualifying', 'Квалификация'),
        ('Sprint', 'Спринт'),
        ('Main', 'Основная гонка'),
        ('Championship', 'Чемпионат'),
    ]

    name = forms.CharField(required=False, label='Название гонки')
    location = forms.CharField(required=False, label='Место проведения')
    race_type = forms.ChoiceField(
        required=False,
        choices=RACE_TYPE_CHOICES,
        label='Тип гонки'
    )