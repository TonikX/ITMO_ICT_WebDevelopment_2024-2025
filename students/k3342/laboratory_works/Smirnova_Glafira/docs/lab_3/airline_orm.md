# Лабораторная работа 3. Реализация серверной части на django rest. ORM модели.

---

## **Описание ORM моделей**

```py
from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.TextField(blank=True)
    contact_info = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Airport(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"


class PlaneModel(models.Model):
    name = models.CharField(max_length=50)
    seats_capacity = models.IntegerField()
    speed = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class Plane(models.Model):
    number = models.CharField(max_length=10, unique=True)
    model = models.ForeignKey(PlaneModel, on_delete=models.CASCADE, related_name='planes')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='planes')

    def __str__(self):
        return f"Plane {self.number} of {self.airline.name}"


class Maintenance(models.Model):
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='maintenances')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'),
                                                      ('Completed', 'Completed')])

    def __str__(self):
        return f"Maintenance for {self.plane.number} ({self.start_date})"


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    education = models.CharField(max_length=255)
    work_experience_years = models.IntegerField()
    passport_data = models.CharField(max_length=20)
    employer = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CrewMember(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='crew_roles')
    role = models.CharField(max_length=50,
                            choices=[('Captain', 'Captain'), ('Co-Pilot', 'Co-Pilot'), ('Navigator', 'Navigator'),
                                     ('Attendant', 'Attendant')])

    def __str__(self):
        return f"{self.employee} ({self.role})"


class Crew(models.Model):
    captain = models.ForeignKey(CrewMember, on_delete=models.SET_NULL, null=True, related_name='captain_of')
    co_pilot = models.ForeignKey(CrewMember, on_delete=models.SET_NULL, null=True, related_name='co_pilot_of')
    navigator = models.ForeignKey(CrewMember, on_delete=models.SET_NULL, null=True, related_name='navigator_of')
    attendants = models.ManyToManyField(CrewMember, related_name='attendant_in')

    def __str__(self):
        return f"Crew with Captain {self.captain.employee}"


class Route(models.Model):
    number = models.CharField(max_length=10, unique=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_routes')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_routes')
    stops = models.ManyToManyField(Airport, related_name='transit_routes', blank=True)
    distance_km = models.FloatField()

    def __str__(self):
        return f"{self.number}: {self.departure_airport} -> {self.destination_airport}"


class Flight(models.Model):
    number = models.CharField(max_length=10, unique=True)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True, related_name='flights')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    plane = models.ForeignKey(Plane, on_delete=models.SET_NULL, null=True, related_name='flights')
    sold_tickets_number = models.IntegerField(default=0)
    status = models.CharField(default='Scheduled', max_length=50,
                              choices=[('Scheduled', 'Scheduled'), ('Boarding', 'Boarding'),
                                       ('Boarding Complete', 'Boarding Complete'), ('In Air', 'In Air'),
                                       ('Landing', 'Landing'), ('Delayed', 'Delayed'), ('Canceled', 'Canceled')])

    def __str__(self):
        return f"Flight {self.number}"


class Seat(models.Model):
    number = models.CharField(max_length=10)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.number} on {self.flight}"


class TransitStop(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='transit_stops')
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='transit_stops')
    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()

    def __str__(self):
        return f"Stop at {self.airport} for {self.flight}"
```