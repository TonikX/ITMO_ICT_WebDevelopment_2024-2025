from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    cars = models.ManyToManyField('Car', through="Ownership")
    passport = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, null=True)
    nationality = models.CharField(max_length=30, null=True)


class DriverLicense(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver_license_id = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()


class Car(models.Model):
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)
    car_owner = models.ManyToManyField(Owner, through='Ownership')


class Ownership(models.Model):
    car = models.ForeignKey(Car, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
