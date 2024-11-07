from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    TYPE_CHOICES = (
        ('A', 'Arrival'),
        ('D', 'Departure'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    gate_number = models.CharField(max_length=10)


class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    comment_text = models.TextField()
    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))


class Passenger(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=20)
