from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Owner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True)
    cars = models.ManyToManyField('Car', through='Ownership')
    passport = models.CharField(max_length=10)
    address = models.TextField(null=True)
    nationality = models.TextField(null=True)
    groups = models.ManyToManyField(Group, related_name='owner_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='owner_set', blank=True)


class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

class Car(models.Model):
    car_number = models.CharField(max_length=15)
    car_brand = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    colour = models.CharField(max_length=30, null=True)

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField(null=True)
