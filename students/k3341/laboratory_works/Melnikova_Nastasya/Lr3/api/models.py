from django.db import models


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    ]

    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Room {self.number}"


class Guest(models.Model):
    passport_number = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    city_from = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Stay(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.guest} -> {self.room}"


class Staff(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    floor = models.IntegerField()

    def __str__(self):
        return f"{self.staff} - {self.get_weekday_display()} - floor {self.floor}"

