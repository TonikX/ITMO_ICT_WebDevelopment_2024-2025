from django.db import models

class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('mb', 'Minibus'),
        ('nb', 'Normal Bus'),
        ('dd', 'Double-Decker'),
        ('eb', 'Electric Bus'),
    ]

    registration_number = models.CharField(max_length=20, unique=True)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.registration_number} ({self.get_bus_type_display()})"

class Route(models.Model):
    route_number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"Route {self.route_number}: {self.start_point} → {self.end_point}"

class Driver(models.Model):
    DRIVER_CLASS_CHOICES = [
        ('MB', 'Minibus driver'),
        ('NB', 'Normal Bus driver'),
        ('DD', 'Double-Decker driver'),
        ('EB', 'Electric Bus driver')
    ]
    name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, unique=True)
    driver_class = models.CharField(max_length=10, choices=DRIVER_CLASS_CHOICES)
    experience_years = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (Class: {self.get_driver_class_display()})"

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('0', 'Active'),
        ('1', 'Completed'),
        ('2', 'Canceled'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="schedules")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    work_date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Schedule: {self.driver.name} {self.driver.driver_class} - {self.bus.registration_number} {self.bus.bus_type} on {self.work_date}"

class Incident(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="incidents")
    incident_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Incident on {self.incident_date} (Schedule ID: {self.schedule.id})"


