from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    home_address = models.TextField(blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"
    
    def get_current_owner(self):
        """Возвращает текущего владельца автомобиля"""
        current_ownership = self.ownership_set.filter(end_date__isnull=True).first()
        return current_ownership.owner if current_ownership else None
    
    def get_all_owners(self):
        """Возвращает всех владельцев автомобиля (текущего и прошлых)"""
        return self.ownership_set.all().order_by('-start_date')

class CarLicense(models.Model):
    license_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"ВУ {self.number} ({self.type})"

class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Автомобиль')
    start_date = models.DateField(verbose_name='Дата начала владения')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания владения')

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date})"
    
    def is_current(self):
        """Проверяет, является ли владение текущим"""
        return self.end_date is None