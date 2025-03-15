from django.db import models
from django.contrib.auth.models import AbstractUser

class CarOwner(AbstractUser):
    passport_number = models.CharField(max_length=20, unique=True, null=True, blank=True, default="Unknown")
    home_address = models.CharField(max_length=255, null=True, blank=True, default="Unknown")
    nationality = models.CharField(max_length=50, null=True, blank=True, default="Unknown")
    birth_date = models.DateTimeField(null=True, blank=True)
    cars = models.ManyToManyField('Car', through="CarOwnership")


class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type_id = models.CharField(max_length=10)
    issue_date = models.DateTimeField()


class Car(models.Model):
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)
    owners = models.ManyToManyField(CarOwner, through="CarOwnership")


class CarOwnership(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
