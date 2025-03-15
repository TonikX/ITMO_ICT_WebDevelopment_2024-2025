from django.db import models
from django.contrib.auth.models import AbstractUser
from blogfspo import settings

'''
class Owner(models.Model):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True, blank=True)
'''

class Owner(AbstractUser):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=10, default="", blank=True, null=True)
    home_address = models.CharField(max_length=30, default="", blank=True, null=True)
    nationality = models.CharField(max_length=30, default="", blank=True, null=True)

class Car(models.Model):
    gov_number = models.CharField(max_length=15, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True, blank=True)
    member = models.ManyToManyField(Owner, through='Ownership')

class License(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #owner_id = models.ForeignKey(Owner,on_delete=models.CASCADE)
    number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date = models.DateField(null=False)

class Ownership(models.Model):
    #owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True, blank=True)