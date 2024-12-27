from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CarOwner(AbstractUser):
    birth_date = models.DateField(null=True)
    passport_number = models.CharField(max_length=10, default="")
    home_address = models.CharField(max_length=100, default="")
    nationality = models.CharField(max_length=30, default="")
    cars = models.ManyToManyField('Car', through='Ownership')


class Car(models.Model):
    gov_number = models.CharField(max_length=15, null=False)
    car_brand = models.CharField(max_length=20, null=False)
    car_model = models.CharField(max_length=20, null=False)
    car_color = models.CharField(max_length=30, null=True)


class Ownership(models.Model):
    owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)


class DriverLicense(models.Model):
    owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issue_date = models.DateField(null=False)
