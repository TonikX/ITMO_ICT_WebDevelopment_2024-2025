from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Tour(models.Model):
    title = models.CharField(max_length=200)
    countries = models.ManyToManyField(Country)
    description = models.TextField()

    def __str__(self):
        return self.title


class Departure(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.tour.title} ({self.start_date}–{self.end_date})"


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает подтверждения'
        CONFIRMED = 'confirmed', 'Подтверждена'
        REJECTED = 'rejected', 'Отклонена'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    departure = models.ForeignKey(Departure, on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} reserves {self.departure}"

