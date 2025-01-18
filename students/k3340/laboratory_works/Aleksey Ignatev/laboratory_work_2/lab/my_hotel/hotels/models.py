from django.contrib.auth.models import User
from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.TextField()

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='hotels')
    address = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return str(self.name) + " at " + str(self.address)


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    amenities = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')

    class Meta:
        unique_together = ['hotel', 'room_number']

    def __str__(self):
        return f"{self.room_type.name} - {self.room_number} in {self.hotel.name}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')

    start_date = models.DateField()
    end_date = models.DateField()

    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.start_date) + " until " + str(self.end_date)


class Review(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    stay_period = models.TextField()
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.comment
