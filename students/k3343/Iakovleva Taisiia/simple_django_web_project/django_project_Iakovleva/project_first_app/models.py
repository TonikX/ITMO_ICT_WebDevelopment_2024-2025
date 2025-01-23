from django.db import models
from django.contrib.auth.models import AbstractUser

class Car_owner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)  
    nationality = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.birth_date} ({self.passport_number})"

class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number}, {self.color})"

class Ownership(models.Model):
    id_car_owner = models.ForeignKey(Car_owner, on_delete=models.CASCADE, null=True)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.car_owner} owns {self.car} from {self.start_date} to {self.end_date}"

class Driving_licence(models.Model):
    id_car_owner = models.ForeignKey(Car_owner, on_delete=models.CASCADE, null=True)
    license_number = models.CharField(max_length=10)
    tyep = models.CharField(max_length=10)
    issuence_date = models.DateField()