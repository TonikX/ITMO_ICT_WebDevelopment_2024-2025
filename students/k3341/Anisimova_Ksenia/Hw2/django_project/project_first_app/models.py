from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class carOwner(AbstractUser):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    date_Birth = models.DateTimeField()
    passport = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)


class car(models.Model):
    id = models.IntegerField(primary_key=True)
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model =  models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    use = models.ManyToManyField(carOwner,through="possession")


class possession(models.Model):
    id = models.IntegerField(primary_key=True)
    id_owner = models.ForeignKey(carOwner,on_delete=models.CASCADE)
    id_car = models.ForeignKey(car,on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)


class driver_license(models.Model):
    id = models.IntegerField(primary_key=True)
    id_owner = models.ForeignKey(carOwner,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issue = models.DateTimeField()
