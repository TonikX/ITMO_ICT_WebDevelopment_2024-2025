from django.db import models
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    birthday_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=10)
    date_of_issue = models.DateField()

    def __str__(self):
        return f"License {self.license_number} for {self.owner}"


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.state_number}"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date} to {self.end_date or 'present'}"