from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    gate = models.CharField(max_length=10)
    arrival_iata = models.CharField(max_length=3)
    departure_iata = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.flight_number} ({self.airline})"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.CharField(max_length=5)
    service_class = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Бронирование пользователя {self.user.username} на рейс {self.flight.flight_number}"

class Comment(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.rating} от {self.user.username} к рейсу {self.flight.flight_number}"
