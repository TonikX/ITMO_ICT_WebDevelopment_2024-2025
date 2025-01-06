from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model


class Owner(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)
    Passport = models.PositiveIntegerField(null=True, blank=True)
    Nationality = models.TextField(null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    cars = models.ManyToManyField('Car', through='Posession')
    groups = models.ManyToManyField(
        Group,
        related_name='owner_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='owner_set',
        blank=True,
    )


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    colour = models.CharField(max_length=30, null=True)

class Posession(models.Model):
    owner = models.ForeignKey(Owner, null=True, blank=True, on_delete=models.CASCADE)
    owner_car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.CASCADE)
    begin_data = models.DateTimeField()
    end_data = models.DateTimeField(null=True, blank=True)


class Driver_license(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number_license = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    iss = models.DateTimeField()
