from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, passport_number, full_name, password=None):
        if not passport_number:
            raise ValueError("Необходимо указать номер паспорта")
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
        max_length=5,
        unique=True,
        primary_key=True,
        validators=[RegexValidator(regex=r'^\d{5}$', message="Номер паспорта должен состоять из 5 цифр")]
    )
    full_name = models.CharField("ФИО", max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'passport_number'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

class Flight(models.Model):
    flight_number = models.CharField(
        "Номер рейса",
        max_length=4,
        primary_key=True,
        validators=[RegexValidator(regex=r'^\d{4}$', message="Номер рейса должен состоять из 4 цифр")]
    )
    airline = models.CharField("Авиакомпания", max_length=255)
    departure_datetime = models.DateTimeField("Дата и время отлета")
    arrival_datetime = models.DateTimeField("Дата и время прилета")
    gate_number = models.CharField(
        "Номер гейта",
        max_length=2,
        validators=[RegexValidator(regex=r'^[A-ZА-Я]\d$', message="Номер гейта должен быть 1 буква и 1 цифра")]
    )

    def __str__(self):
        return f"Рейс {self.flight_number} - {self.airline}"

class Booking(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, verbose_name="Рейс", on_delete=models.CASCADE)
    booking_number = models.CharField(
        "Номер бронирования",
        max_length=3,
        validators=[RegexValidator(regex=r'^\d{3}$', message="Номер бронирования должен состоять из 3 цифр")]
    )
    ticket_number = models.CharField("Номер билета", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Бронирование {self.booking_number} для {self.user}"

class Review(models.Model):
    booking = models.ForeignKey(Booking, verbose_name="Бронирование", on_delete=models.CASCADE)
    review_date = models.DateField("Дата отзыва", default=timezone.now)
    text = models.TextField("Текст отзыва")
    rating = models.IntegerField(
        "Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Рейтинг от 0 до 10"
    )

    def __str__(self):
        return f"Отзыв от {self.booking.user} на рейс {self.booking.flight}"
