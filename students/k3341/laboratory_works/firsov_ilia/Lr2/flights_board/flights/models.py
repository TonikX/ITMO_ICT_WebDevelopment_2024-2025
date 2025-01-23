from django.contrib.auth.models import User
from django.db import models


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    gate_number = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')
    seat_number = models.CharField(max_length=5)
    ticket_number = models.CharField(max_length=20, blank=True, null=True)  # New field for ticket number
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Flight {self.flight.flight_number} - Seat {self.seat_number}"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment_date = models.DateTimeField(auto_now_add=True)
