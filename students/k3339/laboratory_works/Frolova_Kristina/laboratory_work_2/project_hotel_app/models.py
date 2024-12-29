from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    extras = models.CharField(max_length=100)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

