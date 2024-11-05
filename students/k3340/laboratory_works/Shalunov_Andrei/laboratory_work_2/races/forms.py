from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Registration, Comment, Racer, Automobile, RaceResult
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

        widgets = {
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2025}),
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


class NewRacerRegistrationForm(forms.ModelForm):
    racer = forms.ModelChoiceField(
        queryset=Racer.objects.all(),
        label="Выберите гонщика",
        required=True
    )

    car = forms.ModelChoiceField(
        queryset=Automobile.objects.none(),
        label="Выберите автомобиль",
        required=False
    )

    class Meta:
        model = Registration
        fields = ['racer', 'car']

    def __init__(self, *args, **kwargs):
        race = kwargs.pop('race', None)
        super().__init__(*args, **kwargs)

        # Фильтруем список гонщиков, исключая уже зарегистрированных
        if race:
            registered_racers = Registration.objects.filter(race=race).values_list('racer', flat=True)
            self.fields['racer'].queryset = Racer.objects.exclude(id__in=registered_racers).filter(
                user__first_name__isnull=False,
                user__first_name__gt='',
                user__last_name__isnull=False,
                user__last_name__gt=''
            )

        # Проверка и обновление queryset поля 'car' на основании выбранного гонщика
        if 'racer' in self.data:
            try:
                racer_id = int(self.data.get('racer'))
                self.fields['car'].queryset = Automobile.objects.filter(racers__id=racer_id)
            except (ValueError, TypeError):
                pass  # Если racer_id некорректен, оставляем queryset пустым
        elif self.instance.pk:
            self.fields['car'].queryset = self.instance.racer.cars.all()


class NewRacerResultForm(forms.ModelForm):
    racer = forms.ModelChoiceField(
        queryset=Racer.objects.all(),
        label="Выберите гонщика",
        required=True,
        help_text=""
    )

    car = forms.ModelChoiceField(
        queryset=Automobile.objects.none(),
        label="Выберите автомобиль",
        required=False,
    )

    place = forms.IntegerField(
        label="Место",
        required=True,
        min_value=1,
        help_text=""
    )

    class Meta:
        model = RaceResult
        fields = ['racer', 'place', 'finish_time', 'car']
        labels = {
            'place': 'Место',
            'finish_time': 'Время завершения',
        }

    def __init__(self, *args, **kwargs):
        race = kwargs.pop('race', None)
        super().__init__(*args, **kwargs)

        # Фильтруем список гонщиков, исключая уже существующие
        if race:
            racers_in_race = RaceResult.objects.filter(race=race).values_list('racer', flat=True)
            self.fields['racer'].queryset = Racer.objects.exclude(id__in=racers_in_race).filter(
                user__first_name__isnull=False,
                user__first_name__gt='',
                user__last_name__isnull=False,
                user__last_name__gt=''
            )

            self.occupied_places = set(RaceResult.objects.filter(race=race).values_list('place', flat=True))

        # Проверка и обновление queryset поля 'car' на основании выбранного гонщика
        if 'racer' in self.data:
            try:
                racer_id = int(self.data.get('racer'))
                self.fields['car'].queryset = Automobile.objects.filter(racers__id=racer_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['car'].queryset = self.instance.racer.cars.all()

    def clean_place(self):
        place = self.cleaned_data.get('place')

        if place in self.occupied_places:
            raise forms.ValidationError(f"Место {place} уже занято. Пожалуйста, выберите другое место.")

        return place
