from django.db import models

class CarOwner(models.Model):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateTimeField(null=True)
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    license_plate = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.owner} owns {self.car}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    license_number = models.CharField(max_length=10, null=False)
    category = models.CharField(max_length=10, null=False)
    issue_date = models.DateTimeField(null=False)

    def __str__(self):
        return f"License {self.license_number} for {self.owner}"
