from django.db import models
from django.conf import settings

class Car(models.Model):
    registration_number = models.CharField(max_length=15)
    manufacturer = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return "{} {} {}".format(self.manufacturer, self.model, self.color)

class CarOwner(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    date_of_birth = models.DateField(null=True)
    cars = models.ManyToManyField(Car, through='Ownership', related_name="owners")
    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.date_of_birth)

class DriverLicence(models.Model):
    car_owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False, related_name="driverlicenses")
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)

    def __str__(self):
        return "{} {} {}".format(self.car_owner_id, self.license_number, self.license_type)

class Ownership(models.Model):
    car_owner_id = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False, related_name="ownerships")
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    def __str__(self):
        return "{} owns {}".format(self.car_owner_id.first_name, self.car_id)