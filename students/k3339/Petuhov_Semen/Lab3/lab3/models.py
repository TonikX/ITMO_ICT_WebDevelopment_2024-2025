from django.db import models

class Airline(models.Model):
    company_name = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    number_of_employees = models.IntegerField()

    def __str__(self):
        return self.company_name

class AircraftModel(models.Model):
    model_number = models.IntegerField(primary_key=True)
    manufacturer = models.CharField(max_length=30)
    type = models.CharField(max_length=20)
    number_of_seats = models.IntegerField()
    speed = models.IntegerField()
    purpose = models.CharField(max_length=50)
    fuel_consumption = models.IntegerField()
    payload_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.manufacturer} - {self.type}"

class Aircraft(models.Model):
    onBoard_number = models.CharField(max_length=20, primary_key=True)
    company_name = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_hours = models.IntegerField()
    last_maintenance_date = models.DateField()
    manufacture_date = models.DateField()
    model_number = models.ForeignKey(AircraftModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.onBoard_number

class Airport(models.Model):
    airport_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    number_of_runways = models.IntegerField()
    number_of_transits = models.IntegerField()
    lounge_capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Schedule(models.Model):
    schedule_number = models.IntegerField(primary_key=True)
    total_flight_time_hours = models.IntegerField()
    periodicity = models.IntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airport_number = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule {self.schedule_number}"

class TransitStop(models.Model):
    transit_number = models.IntegerField(primary_key=True)
    schedule_number = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    time_in_airport_minutes = models.IntegerField()
    airport_number = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transit {self.transit_number}"

class Flight(models.Model):
    flight_number = models.IntegerField(primary_key=True)
    onBoard_number = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    schedule_number = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Flight {self.flight_number}"

class Employee(models.Model):
    employee_code = models.IntegerField(primary_key=True)
    company_name = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    flight_hours = models.IntegerField()
    position = models.CharField(max_length=20)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.full_name

class Crew(models.Model):
    crew_number = models.IntegerField(primary_key=True)
    medical_check_date = models.DateField()
    clearance_status = models.IntegerField()
    flight_position = models.CharField(max_length=30)
    flight_number = models.ForeignKey(Flight, on_delete=models.CASCADE)
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Crew {self.crew_number} - Flight {self.flight_number}"

class Ticket(models.Model):
    ticket_number = models.IntegerField(primary_key=True)
    flight_number = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=20)
    boarding_number = models.IntegerField()
    payment_type = models.CharField(max_length=20)
    registration_status = models.CharField(max_length=20)
    passenger_data = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket {self.ticket_number}"

class Client(models.Model):
    passenger_data = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.full_name