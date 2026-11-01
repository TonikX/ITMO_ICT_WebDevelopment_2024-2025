from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер паспорта")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return self.username

class Airline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название авиакомпании")
    code = models.CharField(max_length=5, verbose_name="Код (IATA)")

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airport(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название аэропорта")
    city = models.CharField(max_length=50, verbose_name="Город")
    code = models.CharField(max_length=3, verbose_name="Код аэропорта (IATA)")

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    STATUS_CHOICES = [
        ('ontime', 'По расписанию'),
        ('delayed', 'Задержан'),
        ('cancelled', 'Отменен'),
        ('boarding', 'Посадка'),
        ('departed', 'Вылетел'),
    ]

    flight_number = models.CharField(max_length=10, verbose_name="Номер рейса")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name="Авиакомпания")
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures', verbose_name="Аэропорт вылета")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals', verbose_name="Аэропорт прилета")
    departure_time = models.DateTimeField(verbose_name="Время вылета")
    arrival_time = models.DateTimeField(verbose_name="Время прилета")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ontime', verbose_name="Статус")
    gate = models.CharField(max_length=5, blank=True, null=True, verbose_name="Выход (Gate)")

    def __str__(self):
        return f"{self.flight_number} | {self.departure_airport.code} -> {self.arrival_airport.code}"

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name="Рейс")
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пассажир")
    seat_number = models.CharField(max_length=5, verbose_name="Место")
    booked_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")

    def __str__(self):
        return f"Билет на {self.flight.flight_number} для {self.passenger.username}"