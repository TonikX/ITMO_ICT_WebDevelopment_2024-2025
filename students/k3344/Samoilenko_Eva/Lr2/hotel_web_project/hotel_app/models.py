from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    owner = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    ROOM_TYPE_CHOICES = {
        "Standard Single": "Standard Single",
        "Standard Double": "Standard Double",
        "Standard Twin": "Standard Twin",
        "Quadruple Room": "Quadruple Room",
        "Presidential Suit": "Presidential Suit"
    }
    room_type = models.CharField(max_length=17, choices=ROOM_TYPE_CHOICES, default="SS")
    price = models.PositiveIntegerField()
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=100, blank=True, null=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
