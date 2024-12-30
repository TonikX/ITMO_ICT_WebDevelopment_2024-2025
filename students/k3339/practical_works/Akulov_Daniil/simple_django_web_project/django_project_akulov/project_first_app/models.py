from django.db import models
from django.contrib.auth.models import AbstractUser
from django_project_akulov import settings

class Car(models.Model):
    number = models.CharField(max_length=15, null=False)
    mark = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

class Owner(AbstractUser):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True)
    cars = models.ManyToManyField(Car, through="Ownership")
    passport = models.CharField(max_length=30, default="")
    address = models.CharField(max_length=50, default="")
    nationality = models.CharField(max_length=30, default="")

class License(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    receiving_date = models.DateField(null=False)

class Ownership(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)