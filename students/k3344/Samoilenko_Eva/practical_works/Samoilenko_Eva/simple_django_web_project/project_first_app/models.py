from django.db import models
from django.contrib.auth.models import AbstractUser
from django_project_Samoilenko import settings


class Car(models.Model):
    gov_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)


# class Owner(models.Model):
class Owner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    dob = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=10, default="", blank=True, null=True)
    home_address = models.CharField(max_length=30, default="", blank=True, null=True)
    nationality = models.CharField(max_length=30, default="", blank=True, null=True)
    cars = models.ManyToManyField(Car, through='Ownership')


class License(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date = models.DateField()


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_b = models.DateField()
    date_e = models.DateField(null=True, blank=True)
