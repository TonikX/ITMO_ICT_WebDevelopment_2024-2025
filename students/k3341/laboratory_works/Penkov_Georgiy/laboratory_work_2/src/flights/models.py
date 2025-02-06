from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

User = get_user_model()


class Airline(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Flight(models.Model):
    number = models.CharField(max_length=6, unique=True, null=False, blank=False)
    FLIGHT_TYPE = {
        "DEPARTURE": "Departure",
        "ARRIVAL": "Arrival",
    }
    flight_type = models.CharField(
        max_length=10, choices=FLIGHT_TYPE, null=False, blank=False
    )
    direction = models.CharField(max_length=100, null=False, blank=False)
    datetime = models.DateTimeField(null=False, blank=False)
    airline = models.ForeignKey(
        Airline, null=False, blank=False, on_delete=models.CASCADE
    )
    gate = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.number}, {self.direction}"


class PassengerRegistration(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    REGISTRATION_STATUS = {
        "RESERVED": "Reserved",  # пользователь зарезервировал место на рейсе
        "REGISTERED": "Registered",  # админ зарегистрировал пассажира на рейс
    }
    status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS,
        null=False,
        blank=True,
        default="RESERVED",
    )
    ticket = models.CharField(max_length=13, null=True, blank=True)
    seat = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.flight}, {self.passenger}"


class Feedback(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=True)
    rating = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    created_at = models.DateTimeField(null=False, blank=True, default=now)
