from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)
    car_owner = models.ManyToManyField('CarOwner', through='Ownership')
    def __str__(self):
        return f"Автомобиль марки {self.brand} модель {self.model} с гос. номером {self.license_plate}"


class CarOwner(AbstractUser):
    surname = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    date_of_birth = models.DateField(null=False)
    passport = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    nationality = models.CharField(max_length=30, null=True)
    cars = models.ManyToManyField('Car', through="Ownership")
    def __str__(self):
        return f"Автовладелец {self.surname} {self.name} | id - {self.pk}"


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    begin_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.owner.name} owns/owned {self.car} from {self.begin_date} to {self.end_date}"


class DrivingLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    license_number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    issue_date = models.DateField(null=False)
    def __str__(self):
        return f"в/у номер {self.license_number}"
