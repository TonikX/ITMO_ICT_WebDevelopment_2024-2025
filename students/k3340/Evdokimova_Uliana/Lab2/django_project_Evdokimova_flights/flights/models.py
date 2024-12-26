from django.contrib.auth.models import User
from django.db import models

class Flight(models.Model):
    FLIGHT_TYPE_CHOICES = [
        ('arrival', 'Arrival'),
        ('departure', 'Departure'),
    ]
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    flight_type = models.CharField(max_length=10, choices=FLIGHT_TYPE_CHOICES)
    gate_number = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"

class Reservation(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"Reservation for {self.user} on {self.flight}"

class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Review by {self.user} for {self.flight}"

class Passenger(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.reservation.user} - {self.ticket_number}"