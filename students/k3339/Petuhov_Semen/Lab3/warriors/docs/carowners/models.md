# Запросы к базе данных

```python
class CarOwner(models.Model):
    id_owner = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    birthDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name}"


class Vehicle(models.Model):
    id_vehicle = models.AutoField(primary_key=True)
    gosNumber = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.color} ({self.gosNumber})"


class Ownership(models.Model):
    id_owner_car = models.AutoField(primary_key=True)
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships')
    id_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='ownerships')
    data_start = models.DateTimeField(default=timezone.now)
    data_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id_owner} owns {self.id_vehicle}"


class DriveLicense(models.Model):
    id_license = models.AutoField(primary_key=True)
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    data_issue = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.license_number} ({self.type})"
```