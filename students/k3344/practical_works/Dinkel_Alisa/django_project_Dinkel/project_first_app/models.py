from django.db import models


class CarOwner(models.Model):
    id_owner = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} (id: {self.id_owner})"


class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=15, unique=True)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} / ({self.license_plate}) / (id: {self.id_car})"


class Ownership(models.Model):
    id_ownership = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date} - {self.end_date}) / (id: {self.id_ownership}))"


class DriverLicense(models.Model):
    id_license = models.AutoField(primary_key=True)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name="license")
    license_number = models.CharField(max_length=10, unique=True)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"({self.owner}) / ({self.license_number}) / (id: {self.id_license})"

