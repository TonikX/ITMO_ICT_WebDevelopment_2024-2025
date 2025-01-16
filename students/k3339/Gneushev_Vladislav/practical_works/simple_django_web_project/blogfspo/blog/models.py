from django.db import models
from django.contrib.auth.models import AbstractUser

from blogfspo import settings


class CarOwner(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=11, null=True, blank=True)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Car(models.Model):
    state_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=False)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Ownership')

    def __str__(self):
        return f'{self.state_number} - {self.brand} {self.model} ({self.color})'
    

class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.owner} - {self.car} ({self.start_date} - {self.end_date if self.end_date else "now"})'
    

class DriverLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issued_at = models.DateField(null=False)

    def __str__(self):
        return f'{self.owner} - {self.number} ({self.license_type})'
    