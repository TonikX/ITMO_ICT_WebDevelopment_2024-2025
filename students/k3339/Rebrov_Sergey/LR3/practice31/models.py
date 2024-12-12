from django.db import models
from django.db.models import Min, Max, Avg, Count


class Owner(models.Model):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"({self.last_name} {self.first_name})"


class Car(models.Model):
    number = models.CharField(max_length=15, null=False)
    mark = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"({self.number} {self.mark} {self.model})"


class CarOwner(models.Model):
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE, related_name="car_owner")
    car = models.ForeignKey(Car, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"({self.owner} {self.car})"


class License(models.Model):
    owner = models.ForeignKey(Owner, null=False, on_delete=models.CASCADE, related_name="license_owner")
    number = models.CharField(max_length=10, null=False)
    type = models.CharField(max_length=10, null=False)
    date = models.DateField(null=False)

    def __str__(self):
        return f"({self.owner} {self.number} {self.type})"
