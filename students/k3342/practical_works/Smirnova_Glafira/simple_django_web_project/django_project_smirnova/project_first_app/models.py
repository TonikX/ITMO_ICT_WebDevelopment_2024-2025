from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(AbstractUser):
    birth_date = models.DateField(null=True)
    passport_number = models.CharField(max_length=10, default="")
    address = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    nationality = models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    state_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)
    owners = models.ManyToManyField(
        "Owner",
        through="Ownership",
        related_name="cars",
    )

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"


class DriverLicense(models.Model):
    license_number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="licenses", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.license_number} {self.owner.last_name} {self.owner.first_name}"


class Ownership(models.Model):
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True)
    car = models.ForeignKey(Car, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
