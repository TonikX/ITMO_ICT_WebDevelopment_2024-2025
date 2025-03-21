from django.db import models

class CarOwner(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    date_birth = models.DateField(null=True)
    cars = models.ManyToManyField('Car', through='Ownership')

    def __str__(self):
        return f'{self.surname} {self.name}'

class DrivingLicense(models.Model):
    owner = models.ForeignKey(CarOwner, null=True, on_delete=models.CASCADE)
    code_license = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issuing = models.DateField()

    def __str__(self):
        return f'{self.type} {self.code_license}'

class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.brand} {self.state_number}'

class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(null=True)

    def __str__(self):
        return f'{self.owner} owns {self.car}'
