# Формы

## Описание

Реализовать формы для приложения.

## Стек

- Язык: Python
- Библиотека: django

## Листинг

### forms.py:

### Форма для нового юзера:

```python
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'lastname', 'first_name', 'passport')
```
### Форма для комментария

```python
class FeedbackForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=100)
    rating = forms.IntegerField(label='Rating', validators=[
        MaxValueValidator(10),
        MinValueValidator(1)
    ])

    date = forms.DateField(
        label='Flight date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%d'],
    )

```
### Форма для изменения билета:

```python
class TicketUpdateForm(forms.Form):
    seat = forms.CharField(label='Seat', max_length=3)

```
### Форма для бронирования:

```python
class BookForm(forms.Form):
    type = forms.ChoiceField(choices=(('TO', 'Arrival'),
                                      ('FROM', 'Departure')))
    seat = forms.CharField(label="Seat", max_length=3)
```