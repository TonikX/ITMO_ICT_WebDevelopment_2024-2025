from django.contrib.auth.models import AbstractUser
from django.db import models

from Lr2 import settings


# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    cars = models.ManyToManyField('Auto', through='Auto_owner')

    def str(self):
        return f"{self.username}"

class Auto(models.Model):
    gov_number = models.CharField(max_length=15)
    type_of_car = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

class Auto_owner(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    start = models.DateField(null=True)
    end = models.DateField(null=True)

class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    num_of_Document = models.CharField(max_length=10)
    type_of_doc = models.CharField(max_length=10)
    date_of_ownership = models.DateField()


