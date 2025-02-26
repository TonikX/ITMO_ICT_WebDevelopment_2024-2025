from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Car(models.Model):
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model}"


class CarOwner(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    cars = models.ManyToManyField(Car, through='Ownership')
    passport_data = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriverLicense(models.Model):
    TYPE_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )
    car_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_of_issue = models.DateField()


class Ownership(models.Model):
    car_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
