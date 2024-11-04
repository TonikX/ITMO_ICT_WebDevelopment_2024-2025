from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    airline = models.CharField("Авиакомпания", max_length=100)
    flight_number = models.CharField("Номер рейса", max_length=10, unique=True)
    departure_city = models.CharField("Город вылета", max_length=100)
    arrival_city = models.CharField("Город прилета", max_length=100)
    departure_time = models.DateTimeField("Время вылета")
    arrival_time = models.DateTimeField("Время прилета")
    gate_number = models.CharField("Номер гейта", max_length=10, blank=True, null=True)
    flight_type = models.CharField("Тип рейса", max_length=10, choices=[("departure", "Вылет"), ("arrival", "Прилет")])

    def __str__(self):
        return f"{self.flight_number} - {self.airline}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservations")
    seat_number = models.CharField("Номер места", max_length=5)
    reservation_date = models.DateTimeField("Дата бронирования", auto_now_add=True)

    class Meta:
        unique_together = ('user', 'flight', 'seat_number')

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.flight.flight_number}"


class Passenger(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="passengers")
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    ticket_number = models.CharField("Номер билета", max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review_date = models.DateField("Дата рейса")
    comment = models.TextField("Комментарий")
    rating = models.PositiveSmallIntegerField("Рейтинг", choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"Review by {self.user.username} on {self.flight.flight_number}"
