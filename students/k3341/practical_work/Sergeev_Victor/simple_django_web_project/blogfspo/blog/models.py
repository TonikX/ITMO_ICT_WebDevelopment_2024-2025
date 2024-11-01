from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)

class CarOwner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Car(models.Model):
    gov_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    owners = models.ManyToManyField(CarOwner, through='Ownership')

class DriverLicence(models.Model):
    owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    licence_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_of_issue = models.DateField()

class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    date_of_start = models.DateField()
    date_of_finish = models.DateField(null=True, blank=True)

