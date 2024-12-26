from django.contrib.auth.models import AbstractUser
from django.db import models

from django_project_kuznetsov import settings


class Car(models.Model):
    license_plate = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.license_plate} {self.brand} {self.model} {self.color}"


class Owner(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True, blank=True)
    cars = models.ManyToManyField(Car, through='Ownership')
    passport_number = models.CharField(max_length=10, blank=True, null=True)
    home_address = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class DriverLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="driverlicense")
    license_number = models.CharField(max_length=10, null=False)
    category = models.CharField(max_length=10, null=False)
    issue_date = models.DateField(null=False)

    def __str__(self):
        return f"№{self.license_number} {self.category} - {self.owner} - {self.issue_date}"


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships")
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)

    def __str__(self):
        date_end_str = self.date_end if self.date_end else ""
        return f"{self.owner} {self.car.license_plate} ({self.date_start} - {date_end_str})"
