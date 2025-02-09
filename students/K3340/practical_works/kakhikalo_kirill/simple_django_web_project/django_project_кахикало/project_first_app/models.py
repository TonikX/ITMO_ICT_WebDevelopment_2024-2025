from django.db import models

class AutoOwner(models.Model):
    id_owner = models.IntegerField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)

class Auto(models.Model):
    id_auto = models.IntegerField(primary_key=True)
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

class Ownership(models.Model):
    id_ownership = models.IntegerField(primary_key=True)
    id_owner = models.ForeignKey(AutoOwner, on_delete=models.CASCADE, null=True)
    id_auto = models.ForeignKey(Auto, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

class DriverLicense(models.Model):
    id_license = models.IntegerField(primary_key=True)
    id_owner = models.ForeignKey(AutoOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_of_issue = models.DateField()