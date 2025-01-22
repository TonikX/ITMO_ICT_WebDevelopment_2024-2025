from django.db import models
from django.contrib.auth.models import AbstractUser
from djangoProject import settings


class DriverLicense(models.Model):
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Ownership')

    def __str__(self):
        return "{}".format(self.state_number)


class User(AbstractUser):
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    passport_number = models.CharField(max_length=15, null=True, blank=True)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    cars = models.ManyToManyField(Car, through='Ownership')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()





