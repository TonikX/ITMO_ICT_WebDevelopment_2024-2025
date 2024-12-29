from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    info = models.TextField()

    def __str__(self):
        return f"{self.address} {self.phone} {self.country} {self}"


class AircraftType(models.Model):
    model = models.CharField(max_length=255)
    seats = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.model} {self.seats}"


class Airplane(models.Model):
    number = models.CharField(max_length=50)
    type = models.ForeignKey(AircraftType, on_delete=models.CASCADE, related_name='airplanes')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    seats = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    is_in_repair = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number} {self.type}"


class Route(models.Model):
    departure_airport = models.CharField(max_length=100)
    destination_airport = models.CharField(max_length=100)
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.departure_airport}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    sold_tickets = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.flight_number} {self.route}"


class TransitStop(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='transit_stops')
    stop_airport = models.CharField(max_length=100)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.flight} {self.stop_airport} {self.arrival_time}"


class Employee(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='employees')
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    education = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    passport = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} {self.age}"


class Crew(models.Model):
    navigator = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='navigated_crews')
    second_pilot = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='second_pilot_crews')

    def __str__(self):
        return f"{self.navigator}"


class CrewEmployee(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='crew_members')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='crew_roles')
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.crew} {self.employee}"


class FlightInstance(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='instances')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    actual_departure_time = models.DateTimeField(null=True, blank=True)
    actual_arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100)
    seats_sold = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.departure_time}"