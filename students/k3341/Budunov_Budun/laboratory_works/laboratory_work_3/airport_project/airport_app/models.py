from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    registered_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="registered_users")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    def __str__(self):
        return self.username
    
class Airline(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    type = models.BigIntegerField()

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    ROLES = [
    ("Pilot", "Pilot"),
    ("Co-Pilot", "Co-Pilot"),
    ("Flight Attendant", "Flight Attendant"),
    ("Flight Engineer", "Flight Engineer"),
    ("Navigator", "Navigator"),
    ("Loadmaster", "Loadmaster"),
    ("Stewardess", "Stewardess"),
    ("admin", "Administrator"),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True, blank=True)

    # Дополнительные поля для отображения в личном кабинете
    education = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)

    # Поля, требующие одобрения при изменении
    role = models.CharField(max_length=50, choices=ROLES)
    birth_date = models.DateField()
    full_name = models.CharField(max_length=255)
    passport_data = models.CharField(max_length=255)

    # Дополнительные поля для отслеживания изменений
    pending_role = models.CharField(max_length=50, null=True, blank=True)
    pending_birth_date = models.DateField(null=True, blank=True)
    pending_full_name = models.CharField(max_length=255, null=True, blank=True)
    pending_passport_data = models.CharField(max_length=255, null=True, blank=True)

    # Поле для отслеживания статуса запроса
    change_requested = models.BooleanField(default=False)
    request_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Airport(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Route(models.Model):
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_routes')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_routes')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_time = models.DurationField()
    periodicity = models.CharField(max_length=255)
    transit_id_sequence = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.departure_airport} -> {self.arrival_airport})"

class Transit(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='transits')
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='transit_departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='transit_arrivals')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    transit_order = models.IntegerField()

    def __str__(self):
        return f"Transit {self.transit_order} ({self.departure_airport} -> {self.arrival_airport})"

class AirplaneModel(models.Model):
    speed = models.IntegerField()
    seats = models.IntegerField()
    name = models.CharField(max_length=255)
    year_of_manufacture = models.DateTimeField()
    manufacture_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Airplane(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=255)
    airplane_model = models.ForeignKey(AirplaneModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.serial_number} ({self.airplane_model})"

class AirplaneMaintenance(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    is_completed = models.BooleanField()
    notes = models.TextField()

    def __str__(self):
        return f"Maintenance on {self.airplane.serial_number} ({'Completed' if self.is_completed else 'Pending'})"

class Crew(models.Model):
    is_approved = models.BooleanField()

    def __str__(self):
        return f"Crew {'Approved' if self.is_approved else 'Not Approved'}"

class CrewMember(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='members')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.employee.full_name} ({self.role})"

class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    sold_tickets = models.IntegerField()
    flight_number = models.CharField(max_length=255)
    flight_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Flight {self.flight_number} ({self.route})"
