from django.db import models
from django.contrib.auth.models import AbstractUser

class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    mark = models.CharField(max_length=20)


class Affiliation(models.Model):
    owner_id = models.ForeignKey('Owner', on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Owner(AbstractUser):
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    birthdate = models.DateField(null=True, blank=True, default='2000-01-01')
    nation = models.CharField(max_length=20)
    pasport_number = models.CharField(max_length=15)
    addres = models.CharField(max_length=30)


class License(models.Model):
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    release_date = models.DateTimeField()




