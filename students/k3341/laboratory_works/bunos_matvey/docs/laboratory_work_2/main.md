# WEB-программирование

## Лабораторная работа 2: Список отелей

### Задание

Разработать веб-сайт для отображения списка отелей с возможностью резервирования номеров, написания отзывов и управления бронированиями. Основные требования:

- **Модели данных:**
  - **Отель:** название, владелец, адрес, описание, удобства.
  - **Тип номера:** название, вместимость, стоимость, удобства.
  - **Номер:** номер комнаты, связь с типом номера.
  - **Бронирование:** пользователь, номер, даты заезда и выезда, статус заселения.
  - **Отзыв:** связь с бронированием, рейтинг, комментарий.

- **Функционал:**
  - Регистрация пользователей.
  - Просмотр и резервирование номеров.
  - Управление собственными бронированиями (редактирование и удаление).
  - Написание отзывов.
  - Администрирование заселения и выселения пользователей.
  - Отображение списка постояльцев за последний месяц.

### Технологии

- **Backend:** Django 5.1.2
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Frontend:** Bootstrap 5 (для стилизации)
- **Документация:** MkDocs

### Запуск проекта

1. **Установить зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Запустить PostgreSQL с помощью Docker:**

    Выполнить следующую команду:

    ```bash
    ./start_db.sh
    ```

    *Содержимое `start_db.sh`:*

    ```bash
    docker run --name hotel_postgres \
      -e POSTGRES_DB=hotel_db \
      -e POSTGRES_USER=hotel_user \
      -e POSTGRES_PASSWORD=hotel_password \
      -p 5432:5432 \
      -d postgres
    ```

3. **Настроить параметры подключения к базе данных:**

    В `hotel_booking/settings.py` убедится, что секция `DATABASES` настроена следующим образом:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'hotel_db',
            'USER': 'hotel_user',
            'PASSWORD': 'hotel_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

4. **Применить миграции и создать суперпользователя:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. **Запустить сервер разработки:**

    ```bash
    python manage.py runserver
    ```

### Основные компоненты

#### Модели (`bookings/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    amenities = models.TextField()

    def __str__(self):
        return self.name

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='rooms', on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"Комната {self.number} ({self.room_type.name})"

class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"Бронь {self.user.username} - {self.room}"

class Review(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField('Рейтинг', choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.reservation.user.username} - {self.reservation.room}"
```


#### Формы (`bookings/forms.py`)

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ReservationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'check_out': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['check_in'].input_formats = ['%Y-%m-%d']
        self.fields['check_out'].input_formats = ['%Y-%m-%d']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError('Дата выезда должна быть позже даты заезда.')

        conflicts = Reservation.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if conflicts:
            raise forms.ValidationError('Номер недоступен на выбранные даты.')


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
```