from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.conf import settings


class UserManager(DefaultUserManager):
    def create_user(self, passport, password=None, **extra_fields):
        if not passport:
            raise ValueError('The Passport field must be set')
        user = self.model(passport=passport, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, passport, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(passport, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)
    passport = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)

    username = models.CharField(max_length=150, unique=False, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'passport'  # Указываем паспорт как поле для аутентификации
    REQUIRED_FIELDS = []  # Пустой список, если больше полей не требуется

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# class Owner(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     birth_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    

class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    # owner = models.ManyToManyField(Owner, through='Ownership')
    owner = models.ManyToManyField(User, through='Ownership')

    def __str__(self):
        return f"{self.brand} {self.model}"


class Ownership(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} since {self.start_date}"


class License(models.Model):
    LICENSE_TYPE = (
        ('motorcycle', 'A'),
        ('car', 'B'),
        ('truck', 'С'),
        ('bus', 'D')
        )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPE)
    issue_date = models.DateTimeField()

    def __str__(self):
            return f"{self.license_number}, type {self.license_type} ({self.owner.__str__})"



