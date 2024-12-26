from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CarOwner(AbstractUser):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    cars = models.ManyToManyField('Car', through="Ownership")
    birthday_date = models.DateField(null=True)
    nationality = models.CharField(max_length=30, null=True)
    passport = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)


class DriverLicense(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    date = models.DateField()


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    mark = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    car_owner = models.ManyToManyField('CarOwner', through='Ownership')


class Ownership(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
