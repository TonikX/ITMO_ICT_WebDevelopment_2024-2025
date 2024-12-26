from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CarOwner(AbstractUser):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    passport_number = models.IntegerField(null=True)
    address = models.CharField(max_length=100, null=True)
    nationality = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    number = models.CharField(max_length=15)
    label = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Possesion")


class Possesion(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class DriverLicence(models.Model):
    driver_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_of_issue = models.DateField()