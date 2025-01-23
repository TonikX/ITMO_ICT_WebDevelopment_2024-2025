from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Car(models.Model):
    reg_number = models.CharField(max_length=15, unique=True)
    brand = models.CharField(max_length=20)
    model_name = models.CharField(max_length=20)
    color_desc = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.reg_number})"

    def get_full_description(self):
        """Utility method for displaying full car details."""
        return f"{self.brand} {self.model_name}, Color: {self.color_desc or 'N/A'}"


class CarOwner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (ID: {self.user.pk})"


class DrivingLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_num = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=10)
    issued_on = models.DateField()

    def __str__(self):
        return f"License {self.license_num} for {self.owner}"


class Ownership(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    owned_from = models.DateField()
    owned_until = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("car_owner", "vehicle", "owned_from")

    def __str__(self):
        return f"{self.car_owner} - {self.vehicle} from {self.owned_from} to {self.owned_until or 'Present'}"


class User(AbstractUser):
    passport_id = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
