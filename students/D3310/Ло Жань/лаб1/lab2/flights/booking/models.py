from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    flight_type = models.CharField(max_length=10, choices=[('arrival', 'Arrival'), ('departure', 'Departure')])
    gate_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    ticket_number = models.CharField(max_length=20, unique=True)
    seating = models.CharField(max_length=20, choices=[('economy', 'Economy'),
                                                       ('business', 'Business'),
                                                       ('first', 'First')])  # 添加座位类型字段
    passenger_name = models.CharField(max_length=100, null=True)             # 添加乘客姓名字段

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"

class Comment(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.flight.flight_number}"
