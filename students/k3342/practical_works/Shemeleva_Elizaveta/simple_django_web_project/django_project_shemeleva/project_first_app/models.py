from django.db import models
from django.contrib.auth.models import AbstractUser

from django_project_shemeleva import settings


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    address = models.CharField(max_length=255, verbose_name="Домашний адрес")
    nationality = models.CharField(max_length=50, verbose_name="Национальность")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birth_date = models.DateField(null=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.username


class Car(models.Model):
    registration_number = models.CharField(max_length=15, verbose_name="Госномер")
    brand = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, verbose_name="Цвет")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"

class Ownership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    start_date = models.DateField(verbose_name="Дата начала владения")
    end_date = models.DateField(null=True, verbose_name="Дата окончания владения")

    def __str__(self):
        return f"{self.user} владеет {self.car} с {self.start_date} по {self.end_date or 'настоящее время'}"

class DriverLicense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name="Владелец")
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    license_type = models.CharField(max_length=10, verbose_name="Тип")
    issue_date = models.DateField(verbose_name="Дата выдачи")

    def __str__(self):
        return f"{self.license_type} {self.license_number} ({self.user})"
