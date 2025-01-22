from django.db import models
from django.contrib.auth.models import AbstractUser


class Driver(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    passport = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    use = models.ManyToManyField(Driver, through="Ownership")


class Docs(models.Model):
    TYPE_EX = (
      ("t1", "type1"),
      ("t2", "type2"),
      ("t3", "type3"),
    )
    id = models.IntegerField(primary_key=True)
    driver_docs = models.ForeignKey(Driver, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE_EX)


class Ownership(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)