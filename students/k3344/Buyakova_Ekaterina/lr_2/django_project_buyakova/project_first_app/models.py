from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username

class Car(models.Model):
    MAKE_CHOICES = [
        ('Ford', 'Ford'),
        ('Cadillac', 'Cadillac'),
        ('Lincoln', 'Lincoln'),
    ]
    brand = models.CharField(max_length=50, choices=MAKE_CHOICES)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    plate_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"

class Ownership(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date} to {self.end_date}"
