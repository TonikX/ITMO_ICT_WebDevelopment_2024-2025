from django.db import models


class Aircraft(models.Model):
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    seats = models.IntegerField()
    speed = models.IntegerField()
    carrier = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    distance = models.IntegerField()
    departure_point = models.CharField(max_length=50)
    destination_point = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    sold_tickets = models.IntegerField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.flight_number


class CrewMember(models.Model):
    name = models.CharField(max_length=150, default="")
    position = models.CharField(max_length=50)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=150, default="")
    age = models.IntegerField()
    education = models.CharField(max_length=100)
    experience = models.IntegerField()
    passport_data = models.CharField(max_length=20)
    is_airport_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.name
