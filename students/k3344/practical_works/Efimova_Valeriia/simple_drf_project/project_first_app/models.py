from django.contrib.auth.models import AbstractUser
from django.db import models


class Car(models.Model):
    registration_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField()
    cars = models.ManyToManyField(
        Car,
        through="Ownership",
        through_fields=("owner", "car"),
    )


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)


class DrivingLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()


class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20)
    home_address = models.CharField(max_length=100)
    nationality = models.CharField(max_length=30)