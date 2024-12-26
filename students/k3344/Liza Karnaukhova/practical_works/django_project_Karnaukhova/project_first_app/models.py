from django.contrib.auth.models import AbstractUser
from django.db import models
from django_project_Karnaukhova import settings


class Car(models.Model):
    state_number = models.CharField(max_length=10, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)


class Owner(AbstractUser):
    birth_date = models.DateField(null=True)
    passport_number = models.CharField(max_length=10, default="")
    home_address = models.CharField(max_length=30, default="")
    nationality = models.CharField(max_length=30, default="")
    cars = models.ManyToManyField(Car, through='Ownership')


class DriverLicense(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)


class Ownership(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)

