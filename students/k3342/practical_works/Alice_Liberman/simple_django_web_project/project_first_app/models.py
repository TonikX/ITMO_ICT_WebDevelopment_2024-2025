from django.db import models


# Create your models here.
class Owns(models.Model):
    owner_id = models.ForeignKey('Owner',
                                 null=True,
                                 on_delete=models.CASCADE)
    car_id = models.ForeignKey('Car',
                               null=True,
                               on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField(null=True)


class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f'Car: {self.brand}-{self.model}\nLicence plate: {self.license_plate}'


class Owner(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)


class Drivers_license(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_code = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    date_issued = models.DateField()