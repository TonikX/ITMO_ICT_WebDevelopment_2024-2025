from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CarOwnerUser(AbstractUser):
    # Добавляем дополнительные поля
    passport = models.CharField(max_length=10, unique=True, verbose_name="Паспорт", blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, verbose_name="Адрес")
    nationality = models.CharField(max_length=30, blank=True, verbose_name="Национальность")
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Car(models.Model):
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    plate_number = models.CharField(max_length=10, unique=True, verbose_name="Госномер")

    # Связь многие-ко-многим через промежуточную модель Ownership
    owners = models.ManyToManyField(
        CarOwnerUser,
        through='Ownership',
        through_fields=('car', 'owner'),
        verbose_name="Владельцы"
    )

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwnerUser, on_delete=models.CASCADE, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    start_date = models.DateField(verbose_name="Дата начала владения")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания владения")

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date} - {self.end_date})"


class DrivingLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Мотоциклы'),
        ('B', 'Легковые автомобили'),
        ('C', 'Грузовые автомобили'),
        ('D', 'Автобусы'),
    ]

    owner = models.ForeignKey(CarOwnerUser, on_delete=models.CASCADE, verbose_name="Владелец")
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name="Тип")
    issue_date = models.DateField(verbose_name="Дата выдачи")

    def __str__(self):
        return f"{self.license_number} ({self.type}) - {self.owner}"