from django.db import models

class AutoOwner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.birth_date.strftime('%Y-%m-%d')})"

class Car(models.Model):
    registration_number = models.CharField(max_length=15)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"

class Ownership(models.Model):
    owner = models.ForeignKey(AutoOwner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date.strftime('%Y-%m-%d')}"

class DriverLicense(models.Model):
    owner = models.ForeignKey(AutoOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"License {self.license_number} ({self.category}) for {self.owner.first_name} {self.owner.last_name}"
