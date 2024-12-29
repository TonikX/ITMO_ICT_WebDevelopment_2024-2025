from django.db import models
from django.contrib.auth.models import User


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    flight_type = models.CharField(max_length=10, choices=[('departure', 'Отлет'), ('arrival', 'Прилет')])
    gate_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flight.flight_number} - {self.user.username}"
