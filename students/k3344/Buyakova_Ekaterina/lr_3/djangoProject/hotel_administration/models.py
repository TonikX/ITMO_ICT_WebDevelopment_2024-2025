from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['last_name', 'first_name']


class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    TRIPLE = 'Triple'
    ROOM_TYPES = [
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (TRIPLE, 'Triple'),
    ]

    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(unique=True)
    floor = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15, blank=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.number} ({self.type})"


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    passport_number = models.CharField(max_length=15, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.passport_number})"


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.profession})"


class CleaningSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="schedules")
    floor = models.PositiveIntegerField()
    day_of_week = models.CharField(max_length=15)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cleaning_schedules", null=True,
                               blank=True)

    def __str__(self):
        return f"Floor {self.floor} ({self.day_of_week})"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f"Reservation: {self.client} - Room {self.room.number}"


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    quarter = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reports")
    total_clients = models.PositiveIntegerField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Report for {self.quarter} quarter {self.year} - Room {self.room.number}"
