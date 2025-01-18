from django.contrib.auth.models import User
from django.db import models


class Flight(models.Model):
    number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    flight_type = models.CharField(max_length=10, choices=[('departure', 'Departure'), ('arrival', 'Arrival')])
    gate = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.number} - {self.airline}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"Reservation: {self.user.username} - {self.flight.number} ({self.seat_number})"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review by {self.user.username} - {self.flight.number} ({self.rating}/10)"
