from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20, unique=True)
    home_address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField(null=False, blank=True)

    def __str__(self):
        return self.username


class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    ownership_id = models.AutoField(primary_key=True, db_column="id_владельца_авто")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="id_владельца")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column="id_автомобиля")
    start_date = models.DateTimeField(db_column="дата_начала")
    end_date = models.DateTimeField(null=True, blank=True, db_column="дата_окончания")

    def __str__(self):
        return f"{self.owner} owns {self.car}"


class DriverLicense(models.Model):
    license_id = models.AutoField(primary_key=True, db_column="id_удостоверения")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="id_владельца")
    license_number = models.CharField(max_length=10, unique=True, db_column="номер_удостоверения")
    license_type = models.CharField(max_length=10, db_column="тип")
    issue_date = models.DateTimeField(db_column="дата_выдачи")

    def __str__(self):
        return f"{self.license_number} ({self.license_type})"
