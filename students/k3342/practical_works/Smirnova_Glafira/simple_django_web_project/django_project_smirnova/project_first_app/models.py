from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(AbstractUser):
    birth_date = models.DateField(null=True)
    passport_number = models.CharField(max_length=10, default="")
    cars = models.ManyToManyField('Car', through="Ownership")
    address = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    nationality = models.CharField(max_length=30, null=True)


class Car(models.Model):
    state_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)
    car_owner = models.ManyToManyField(Owner, through='Ownership')


class DriverLicense(models.Model):
    license_number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ownership(models.Model):
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)
    car_id = models.ForeignKey(Car, null=True, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
