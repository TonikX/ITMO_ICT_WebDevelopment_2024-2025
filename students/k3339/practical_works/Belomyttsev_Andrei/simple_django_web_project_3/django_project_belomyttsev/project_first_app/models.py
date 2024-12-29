from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Car(models.Model):
  number = models.CharField(max_length=15, null=False, blank=False)
  brand = models.CharField(max_length=20, null=False, blank=False)
  model = models.CharField(max_length=20, null=False, blank=False)
  color = models.CharField(max_length=30, null=True, blank=True)

  def __str__(self):
    return f'{self.number}, {self.brand}, {self.model}'

class Owner(AbstractUser):
  last_name = models.CharField(max_length=30, null=False, blank=False)
  first_name = models.CharField(max_length=30, null=False, blank=False)
  date_of_birth = models.DateField(null=True, blank=True)
  cars = models.ManyToManyField(Car, through='Ownership', null=True, blank=True)

  passport_number = models.CharField(max_length=30, null=True, blank=True)
  home_address = models.CharField(max_length=100, null=True, blank=True)
  nationality = models.CharField(max_length=30, null=True, blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

class License(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=False, blank=False)
  number = models.CharField(max_length=10, null=False, blank=False)
  type = models.CharField(max_length=10, null=False, blank=False)
  date_of_issue = models.DateField(null=False, blank=False)

  def __str__(self):
    return f'{self.owner}'

class Ownership(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, blank=True)
  car = models.ForeignKey(Car, models.CASCADE, null=True, blank=True)
  start_date = models.DateField(null=False, blank=False)
  end_date = models.DateField(null=True, blank=True)

  def __str__(self):
    return f'{self.car.number}, {self.owner}, {self.start_date} - {self.end_date}'