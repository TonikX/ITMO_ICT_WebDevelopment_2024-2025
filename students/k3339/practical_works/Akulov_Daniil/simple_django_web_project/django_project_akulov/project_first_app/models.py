from django.db import models

class Owner(models.Model):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True)

class License(models.Model):
    id_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    receiving_date = models.DateField(null=False)

class Car(models.Model):
    number = models.CharField(max_length=15, null=False)
    mark = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

class Ownership(models.Model):
    id_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)