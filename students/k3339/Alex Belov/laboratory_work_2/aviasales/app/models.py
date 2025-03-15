from django.contrib.auth.models import User
from django.db import models

class Airline(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Aircraft(models.Model):
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.brand}, {self.model}"

class Places(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.RESTRICT)
    row = models.IntegerField()
    col = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.row}-{self.col}"

class Races(models.Model):
    race_code = models.CharField(max_length=10)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.RESTRICT)
    airline = models.ForeignKey(Airline, on_delete=models.RESTRICT)
    is_departure = models.BooleanField()
    date = models.DateTimeField()

    def __str__(self):
        return f"[{"DEPARTURE" if self.is_departure else "ARRIVAL"}] {self.race_code} ({self.airline}, {self.aircraft}, {self.date})"

class Ticket(models.Model):
    race = models.ForeignKey(Races, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

class Bookings(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now=True)
    place = models.ForeignKey(Places, on_delete=models.RESTRICT)

class Review(models.Model):
    race = models.ForeignKey(Races, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=500)
    rating = models.IntegerField()
