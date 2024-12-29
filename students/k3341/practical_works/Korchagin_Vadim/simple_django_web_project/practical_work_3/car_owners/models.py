from django.contrib.auth.models import AbstractUser
from django.db import models

class CarOwner(AbstractUser):
    birth_date = models.DateTimeField(null=True)
    passport_number = models.CharField(max_length=10, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    cars = models.ManyToManyField('Car', through='Ownership')


class Car(models.Model):
    license_plate = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

class Ownership(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True)


class DriverLicense(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issue_date = models.DateTimeField(null=False)