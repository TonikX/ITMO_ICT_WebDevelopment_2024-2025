from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

class Hotel(models.Model):
    name = models.CharField(max_length=144, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    address = models.CharField(max_length=144)
    description = models.CharField(max_length=400)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    room_type = models.CharField(max_length=25)
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def is_finished(self):
        return timezone.now() > self.check_out

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    text = models.CharField(max_length=400)
    rating = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])