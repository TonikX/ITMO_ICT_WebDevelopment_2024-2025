from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Car(models.Model):
    license_plate = models.CharField(max_length=15, verbose_name="License Plate")
    brand = models.CharField(max_length=20, verbose_name="Brand")
    model = models.CharField(max_length=20, verbose_name="Model")
    color = models.CharField(max_length=30, null=True, verbose_name="Color")


class Owner(AbstractUser):
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    birth_date = models.DateTimeField(verbose_name="Birth Date", null=True)
    passport_number = models.CharField(max_length=10, verbose_name="Passport Number")
    home_address = models.CharField(max_length=255, verbose_name="Home Address")
    nationality = models.CharField(max_length=50, verbose_name="Nationality")
    cars = models.ManyToManyField(Car, through='Ownership')


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner ID")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Car ID")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(null=True, verbose_name="End Date")


class DriversLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner ID")
    license_number = models.CharField(max_length=10, verbose_name="License Number")
    license_type = models.CharField(max_length=10, verbose_name="Type")
    issue_date = models.DateTimeField(verbose_name="Issue Date")
