from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Registration, Comment, Racer, Automobile
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text=""
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text=""
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }
        help_texts = {
            'username': "",
        }


class RegistrationForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        queryset=Automobile.objects.none(),
        required=True,
        label="Выберите автомобиль"
    )

    class Meta:
        model = Registration
        fields = ['car']

    def __init__(self, *args, **kwargs):
        racer = kwargs.pop('racer', None)
        super().__init__(*args, **kwargs)
        if racer:
            # Устанавливаем queryset для поля car, чтобы он содержал только автомобили гонщика
            self.fields['car'].queryset = racer.cars.all()


class UnregisterForm(forms.Form):
    pass


class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1,11)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, label="Рейтинг")

    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        labels = {
            'text': 'Текст комментария',
            'comment_type': 'Тип комментария',
        }


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team_name', 'experience', 'racer_class']
        labels = {
            'team_name': 'Название команды',
            'experience': 'Опыт (лет)',
            'racer_class': 'Класс гонщика',
        }
        widgets = {
            'team_name': forms.TextInput(attrs={'placeholder': 'Введите название команды'}),
            'experience': forms.NumberInput(attrs={'min': 0}),
            'racer_class': forms.TextInput(attrs={'placeholder': 'Введите свой класс'}),
        }


class AutomobileForm(forms.ModelForm):
    class Meta:
        model = Automobile
        fields = ['brand', 'model', 'year', 'description']
        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Год выпуска',
            'description': 'Описание',
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RacerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team_name', 'experience', 'racer_class', 'cars']
        widgets = {
            'cars': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cars'].queryset = user.racer.cars.all()
