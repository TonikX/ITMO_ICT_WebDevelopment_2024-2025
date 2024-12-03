from django.db import models
# from django.contrib.auth.models import User


class Client(models.Model):
    passport_number = models.CharField(max_length=11)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, blank=True, null=True,
                                   verbose_name="Middle/Father's name")
    origin_city = models.CharField(max_length=50)

    def __str__(self):
        return f'Client {self.first_name} {self.last_name}'


class Hotel(models.Model):
    num_rooms = models.SmallIntegerField()

    def __str__(self):
        return 'One and only Hotel'


class Employee(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='employees')
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, blank=True, null=True,
                                   verbose_name="Middle/Father's name")
    is_employed = models.BooleanField(default=True)

    def __str__(self):
        return f'Employee {self.first_name} {self.last_name}'


class Floor(models.Model):
    floor_num = models.SmallIntegerField(primary_key=True, unique=True)

    def __str__(self):
        return str(self.floor_num)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    ROOM_TYPE_CHOICES = {
        "Single": "Single",
        "Double": "Double",
        "Triple": "Triple",
    }
    room_type = models.CharField(max_length=6, choices=ROOM_TYPE_CHOICES, default="Single")
    price = models.PositiveIntegerField()
    phone_num = models.IntegerField()
    floor_num = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="room_floor")

    def __str__(self):
        return f'{self.room_type} on Floor {self.floor_num}'


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="booking_client")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="booking_room")
    start_date = models.DateField()
    end_date = models.DateField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking for {self.client} to Room {self.room}'


class Cleaning(models.Model):
    floor_num = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="cleaning_floor")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 related_name="cleaning_employee")
    WEEK_DAY_CHOICES = (
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    )
    week_day = models.CharField(max_length=3, choices=WEEK_DAY_CHOICES)

    def __str__(self):
        return f'Cleaning of {self.employee} on {self.floor_num} floor on {self.week_day}'
