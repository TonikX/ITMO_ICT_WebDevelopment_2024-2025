from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
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

    def __str__(self):
        return self.username


class Car(models.Model):
    MAKE_CHOICES = [
        ('Toyota', 'Toyota'),
        ('Ford', 'Ford'),
        ('BMW', 'BMW'),
    ]
    make = models.CharField(max_length=50, choices=MAKE_CHOICES)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    state_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.make} {self.model} ({self.state_number})"


class Ownership(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date} to {self.end_date}"
