from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class OwnerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Owner(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=30, null=False, blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=True)
    birth_date = models.DateField(null=False)
    passport_number = models.CharField(max_length=20, null=False, blank=False, unique=True)
    home_address = models.CharField(max_length=20, null=False, blank=False)
    nationality = models.CharField(max_length=20, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'birth_date', 'passport_number', 'home_address', 'nationality']

    objects = OwnerManager()

    def __str__(self):
        return self.email


class Car(models.Model):
    state_num = models.CharField(max_length=15, null=False, blank=False, unique=True)
    brand = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=30, null=False, blank=False)
    owners = models.ManyToManyField(
        Owner,
        through="Ownership",
        related_name="cars",
    )

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_id = models.CharField(max_length=10, null=False, blank=False, unique=True)
    type = models.CharField(max_length=10, null=False, blank=False)
    license_date = models.DateField(null=True, blank=True)
