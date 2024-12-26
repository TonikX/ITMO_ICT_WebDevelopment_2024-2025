from django.db import models

from djangoProject import settings


class CarOwner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birthday_date}'


class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owner = models.ManyToManyField(CarOwner, through='Ownership')

    def __str__(self):
        return "{}".format(self.state_number)


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()





