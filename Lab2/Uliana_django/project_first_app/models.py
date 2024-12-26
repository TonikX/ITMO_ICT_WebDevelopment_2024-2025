from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, unique=True)
    home_address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} - {self.nationality}"

class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.owner} owns {self.car}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"License {self.license_number} of {self.owner}"
