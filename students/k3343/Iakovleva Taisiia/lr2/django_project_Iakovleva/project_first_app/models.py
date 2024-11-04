from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    passport = models.CharField(max_length=20, blank=True, null=True) 
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True) 
    airline = models.CharField(max_length=50) 
    departure_time = models.DateTimeField()  
    arrival_time = models.DateTimeField() 
    flight_type = models.CharField(max_length=10, choices=[('departure', 'Отлет'), ('arrival', 'Прилет')]) 
    gate_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE) 
    seat_number = models.CharField(max_length=5)
    ticket_number = models.CharField(max_length=20, unique=True)
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation: {self.user.username} - {self.flight.flight_number} ({self.seat_number})"

class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    review_date = models.DateTimeField(auto_now_add=True) 
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])

    def __str__(self):
        return f"Review by {self.user.username} on {self.flight.flight_number}: {self.rating}"
