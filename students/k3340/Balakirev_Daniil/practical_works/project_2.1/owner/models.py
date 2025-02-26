from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CarOwner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_of_birthday = models.DateField(null=True)
    passport = models.CharField(max_length=30, null=True)
    home_address = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)

class DriversLicense(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issue = models.DateField()

class Car(models.Model):
    car_number = models.CharField(max_length=15)
    mark = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    colour = models.CharField(max_length=30)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, through='OwnerShip')

class OwnerShip(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(null=True)