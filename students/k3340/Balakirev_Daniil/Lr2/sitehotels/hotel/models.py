from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()


class RoomType(models.Model):
    name = models.CharField(max_length=100)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    amenities = models.TextField()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    text = models.TextField()
    rating = models.IntegerField()