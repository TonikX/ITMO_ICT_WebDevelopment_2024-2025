from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True)  # Номер паспорта
    home_address = models.CharField(max_length=255, blank=True, null=True)      # Домашний адрес
    nationality = models.CharField(max_length=50, blank=True, null=True)        # Национальность


# Модель владельца автомобиля
class CarOwner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Связь с пользователем
    first_name = models.CharField(max_length=30, null=False)            # Имя владельца
    last_name = models.CharField(max_length=30, null=False)             # Фамилия владельца
    date_of_birth = models.DateTimeField(null=True)                     # Дата рождения
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')  # Связь с автомобилями через Ownership

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель водительского удостоверения
class IDCard(models.Model):
    license_id = models.AutoField(primary_key=True)                    # Id удостоверения (pk)
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)  # Владелец (FK)
    license_number = models.CharField(max_length=10, null=False)       # Номер удостоверения
    license_type = models.CharField(max_length=10, null=False)         # Тип удостоверения
    issue_date = models.DateTimeField(null=False)                      # Дата выдачи

    def __str__(self):
        return f"ID: {self.license_number} ({self.license_type})"

# Модель автомобиля
class Car(models.Model):
    car_id = models.AutoField(primary_key=True)                        # Id автомобиля (pk)
    registration_number = models.CharField(max_length=15, null=False)  # Гос номер
    make = models.CharField(max_length=20, null=False)                 # Марка
    model = models.CharField(max_length=20, null=False)                # Модель
    color = models.CharField(max_length=30, null=True)                 # Цвет

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"

# Модель владения
class Ownership(models.Model):
    ownership_id = models.AutoField(primary_key=True)                   # Id владения (pk)
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)   # Владелец (FK)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)              # Автомобиль (FK)
    start_date = models.DateTimeField(null=False)                       # Дата начала владения
    end_date = models.DateTimeField(null=True)                          # Дата окончания владения

    def __str__(self):
        return f"Ownership: {self.car_owner} - {self.car} from {self.start_date} to {self.end_date}"
