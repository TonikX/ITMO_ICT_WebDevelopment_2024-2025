from django.db import models
from django.contrib.auth.models import User

class CarOwner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.license_plate})'

class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f'{self.license_number} - {self.owner}'

class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.owner} owns {self.car}'


from django.db import models


class CarOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=20, verbose_name='Номер паспорта')
    address = models.CharField(max_length=255, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, verbose_name='Национальность')

    def __str__(self):
        return f"{self.user.username} - {self.nationality}"
