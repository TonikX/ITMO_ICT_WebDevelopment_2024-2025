from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    address = models.CharField(max_length=255, verbose_name="Домашний адрес")
    nationality = models.CharField(max_length=50, verbose_name="Национальность")

    def __str__(self):
        return f"{self.username} ({self.nationality})"


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    birth_date = models.DateField(null=True, verbose_name="Birth Date")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DrivingLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, unique=True, verbose_name="License Number")
    TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    license_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Type")
    issue_date = models.DateTimeField(verbose_name="Issue Date")

    def __str__(self):
        return f"{self.license_number} ({self.license_type})"


class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True, verbose_name="License Plate")
    make = models.CharField(max_length=20, verbose_name="Make")
    model = models.CharField(max_length=20, verbose_name="Model")
    color = models.CharField(max_length=30, null=True, verbose_name="Color")

    def __str__(self):
        return f"{self.make} {self.model} - {self.license_plate}"


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='owners', verbose_name="Car")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="End Date")

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date}"
