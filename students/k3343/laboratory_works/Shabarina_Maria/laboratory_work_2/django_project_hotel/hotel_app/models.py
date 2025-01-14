from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Hotel(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    address = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('user', 'Regular User'),
        ('admin', 'Hotel Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    managed_hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='admins')


class RoomType(models.Model):
    type = models.CharField(max_length=20)
    description = models.TextField()
    capacity = models.CharField(max_length=100)
    facilities = models.CharField(max_length=100)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.CharField(max_length=100)


class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('checked_in', 'Checked In'), ('checked_out', 'Checked Out')], default='not_checked_in')


class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
