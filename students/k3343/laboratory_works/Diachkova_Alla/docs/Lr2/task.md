### Условие
3. Табло отображения информации об авиаперелетах.
Хранится информация о номере рейса, авиакомпании, отлете, прилете, типе
(прилет, отлет), номере гейта.
Необходимо реализовать следующий функционал:


    Регистрация новых пользователей.
    Просмотр и резервирование мест на рейсах. Пользователь должен иметь
    возможность редактирования и удаления своих резервирований.
    Администратор должен иметь возможность зарегистрировать на рейс
    пассажира и вписать в систему номер его билета средствами Django-admin.
    В клиентской части должна формироваться таблица, отображающая всех
    пассажиров рейса.
    Написание отзывов к рейсам. При добавлении комментариев, должны
    сохраняться дата рейса, текст комментария, рейтинг (1-10), информация о
    комментаторе.
### 
Скрины работы:
Редактирование средстави джанго БД для админа:
![](images/flightapp.png)

Регистрация:
![](images/register.png)

Вход:
![](images/login.png)

Главная страница, до добавления информации
![](images/flights.png)

Страница рейса, до интеракций пользователей с рейсом
![](images/flightpage0.png)

Страница рейса
![](images/flightpage.png)

Листинг кода, models.py: 
``` py hl_lines="2 3"
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, passport_number, full_name, password=None):
        if not passport_number:
            raise ValueError("Passport number is required")
        user = self.model(passport_number=passport_number, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, passport_number, full_name, password):
        user = self.create_user(passport_number, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    passport_number = models.CharField(
        max_length=9,
        unique=True,
        primary_key=True,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Passport number must consist of 9 digits")]
    )
    full_name = models.CharField("Full Name", max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'passport_number'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.full_name


class Flight(models.Model):
    flight_number = models.CharField(
        "Flight Number",
        max_length=4,
        primary_key=True,
        validators=[RegexValidator(regex=r'^\d{4}$', message="Flight number must consist of 4 digits")]
    )
    airline = models.CharField("Airline", max_length=255)
    departure_datetime = models.DateTimeField("Departure Date and Time")
    arrival_datetime = models.DateTimeField("Arrival Date and Time")
    flight_type = models.CharField(
        "Flight Type", max_length=10,
        choices=[('departure', 'Departure'), ('arrival', 'Arrival')]
    )
    gate_number = models.CharField(
        "Gate Number",
        max_length=2,
        validators=[RegexValidator(regex=r'^\d{2}$', message="Gate number must consist of 2 digits")]
    )

    def __str__(self):
        return f"Flight {self.flight_number} - {self.airline}"


class Booking(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, verbose_name="Flight", on_delete=models.CASCADE)
    booking_number = models.CharField(
        "Booking Number",
        max_length=5,
        validators=[RegexValidator(regex=r'^\d{5}$', message="Booking number must consist of 5 digits")]
    )
    ticket_number = models.CharField("Ticket Number", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.booking_number} for {self.user}"


class Review(models.Model):
    booking = models.ForeignKey(Booking, verbose_name="Booking", on_delete=models.CASCADE)
    review_date = models.DateField("Review Date", default=timezone.now)
    text = models.TextField("Review Text")
    rating = models.IntegerField(
        "Rating",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating from 1 to 10"
    )

    def __str__(self):
        return f"Review by {self.booking.user} for flight {self.booking.flight}"

``` 