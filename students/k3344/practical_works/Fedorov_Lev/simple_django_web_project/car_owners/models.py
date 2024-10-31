from django.db import models
from django.contrib.auth.models import AbstractUser, get_user_model
from django.conf import settings

class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20)
    home_address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().id)
    birth_date = models.DateTimeField(null=False, verbose_name="Birth Date")
    email = models.EmailField(null=True, verbose_name="Email")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ['user__last_name', 'user__first_name']

class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True, verbose_name="License Plate")
    brand = models.CharField(max_length=20, verbose_name="Brand")
    model = models.CharField(max_length=20, verbose_name="Model")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Color")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        ordering = ['brand', 'model']


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Owner", related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Car", related_name="ownerships")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="End Date")

    def __str__(self):
        return f"{self.owner} owns {self.car}"

    class Meta:
        verbose_name = "Ownership"
        verbose_name_plural = "Ownerships"
        ordering = ['start_date']


class License(models.Model):
    LICENSE_TYPES = [
        ('A', 'Type A'),
        ('B', 'Type B'),
        ('C', 'Type C'),
        ('D', 'Type D'),
        ('M', 'Type M'),
        ('T', 'Type T'),
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Owner", related_name="licenses")
    license_number = models.CharField(max_length=10, unique=True, verbose_name="License Number")
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name="License Type")
    issue_date = models.DateTimeField(verbose_name="Issue Date")

    def __str__(self):
        return f"{self.license_number} - {self.get_license_type_display()}"

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"
        ordering = ['issue_date']
