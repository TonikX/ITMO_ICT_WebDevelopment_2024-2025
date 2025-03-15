from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_hotels")
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    favorites = models.ManyToManyField(User, related_name="favorite_hotels", blank=True)


class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    SUITE = 'Suite'
    FAMILY = 'Family'

    ROOM_TYPE_CHOICES = [
        (SINGLE, 'Одноместный'),
        (DOUBLE, 'Двухместный'),
        (SUITE, 'Люкс'),
        (FAMILY, 'Семейный'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_hotels')
    type = models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES, default=SINGLE)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username