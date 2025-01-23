# Формы

## TourForm

```python
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'hotel',
            'stars',
            'agency',
            'country',
            'city',
            'description',
            'start_date',
            'end_date',
            'payment_conditions',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Календарь для start_date
            'end_date': forms.DateInput(attrs={'type': 'date'}),    # Календарь для end_date
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        today = date.today()
        if start_date < today:
            raise forms.ValidationError("Start date must be today or later.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date < self.cleaned_data.get('start_date'):
            raise forms.ValidationError("End date cannot be before start date.")
        return end_date
```

- Используется для ввода и редактирования данных модели Tour.
- Включает в себя указанные поля модели Tour.
- Поля start_date и end_date используют HTML-виджет с типом date, который отображает календарь для выбора дат.
- clean_start_date: Проверяет, что дата начала (start_date) не раньше сегодняшнего дня. Если дата не проходит проверку, выбрасывается ошибка.
- clean_end_date: Проверяет, что дата окончания (end_date) не предшествует дате начала. Если это условие нарушено, также выбрасывается ошибка.
- Обеспечивает корректный ввод данных для модели Tour, добавляет выбор дат через календарь и включает проверки на соответствие логическим условиям.

## TariffForm и MealOptionForm

```python
class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price']


class MealOptionForm(forms.ModelForm):
    class Meta:
        model = MealOption
        fields = ['name', 'price']


# Inline formsets для Tariff и MealOption
TariffFormSet = inlineformset_factory(
    Tour, Tariff, form=TariffForm, extra=1, can_delete=True
)
MealOptionFormSet = inlineformset_factory(
    Tour, MealOption, form=MealOptionForm, extra=1, can_delete=True
)
```
Классы TariffForm и MealOptionForm:

- Определяют формы для моделей Tariff и MealOption.
- Указывают, что name и price будут доступны для редактирования.
- 
TariffFormSet и MealOptionFormSet:
- Используют inlineformset_factory для создания инлайновых формсетов, позволяющих редактировать связанные объекты Tariff и MealOption прямо из формы для тура.
- Связь устанавливается через модель Tour.

Настройки:
- form: Используемые формы (TariffForm и MealOptionForm).
- extra=1: При добавлении нового объекта в формсете будет одна пустая форма по умолчанию.
- can_delete=True: Разрешает удаление связанных объектов через форму.

## CustomAuthenticationForm

```python
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
```

Наследуется от AuthenticationForm и кастомизирует поля username и password, добавляя стили и плейсхолдеры для улучшения внешнего вида ввода.

## CustomUserCreationForm

```python
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
```

Наследуется от UserCreationForm и используется для создания нового пользователя с полями username, email, password1, password2.

## BookingForm

```python
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_people', 'tariff', 'meal_option']

    def __init__(self, *args, **kwargs):
        tour = kwargs.pop('tour', None)
        super().__init__(*args, **kwargs)

        if tour:
            # Ограничиваем выбор тарифов и вариантов питания
            self.fields['tariff'].queryset = tour.tariffs.all()
            self.fields['meal_option'].queryset = tour.meal_options.all()

            self.fields['tariff'].widget = forms.Select(
                attrs={
                    'class': 'tariff-select',
                },
                choices=[(tariff.id, f'{tariff.name} - {tariff.price} RUB') for tariff in tour.tariffs.all()]
            )
            self.fields['meal_option'].widget = forms.Select(
                attrs={
                    'class': 'meal-select',
                },
                choices=[(meal.id, f'{meal.name} - {meal.price} RUB') for meal in tour.meal_options.all()]
            )
```

Используется для бронирования тура. Она позволяет выбрать количество людей (num_people), тариф (tariff) и вариант питания (meal_option). В конструкторе формы ограничиваются доступные тарифы и варианты питания в зависимости от выбранного тура.

## ReviewForm

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
```

Используется для создания отзыва. Она включает два поля: текст отзыва и рейтинг. Используется для отправки отзыва о туре, который затем сохраняется в базе данных.

## TourSearchForm

```python
class TourSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
```
Предназначена для поиска туров. Она содержит одно поле query, в котором пользователи могут вводить строку для поиска. Поле имеет максимальную длину 100 символов и не является обязательным для заполнения (required=False).