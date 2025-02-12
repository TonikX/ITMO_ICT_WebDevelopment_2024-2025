from django.db import models
from django.contrib.auth.models import AbstractUser

# Автовладелец
class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Автомобиль
class Car(models.Model):
    car_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    car_model = models.CharField(max_length=20)
    colour = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.car_model} ({self.car_number})"

# Владение
class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownership')
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name='ownership')
    beginning = models.DateField()
    ending = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} владеет {self.car} с {self.beginning} по {self.ending}"

# Водительское удостоверение
class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='license')
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    receiving_date = models.DateField()

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.license_type}) - {self.owner}"

class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20)
    home_address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
