from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CarOwner(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    cars = models.ManyToManyField('Car', through="Ownership")  # Ensure correct intermediate model
    birthday_date = models.DateField(null=True)


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    mark = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    car_owners = models.ManyToManyField(CarOwner, through="Ownership")  # Fix naming


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)  # Fix: Use CarOwner instead of AUTH_USER_MODEL
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Fix: Ensure end_date allows null


class DriverLicense(AbstractUser):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    date = models.DateField()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="+",  # Prevents reverse accessor conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="+",  # Prevents reverse accessor conflicts
        blank=True
    )
