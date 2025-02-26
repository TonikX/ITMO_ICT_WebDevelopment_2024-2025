from django.db import models

class Client(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    cleaning_status = models.CharField(max_length=50, default="Clean")
    is_occupied = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"


class RoomPrice(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('room_type','start_date', 'end_date')

    def __str__(self):
      return f"Price for {self.room_type.name} from {self.start_date} to {self.end_date}: {self.price}"


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    booking_status = models.CharField(max_length=50, default="Booked")
    payment_status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Booking for {self.client} in {self.room} on {self.booking_date}"


class JobTitle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Employee(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmploymentContract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Contract for {self.employee} as {self.job_title}"


class CleaningSchedule(models.Model):
    cleaning_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Scheduled")
    cleaner = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cleaning schedule for {self.room} on {self.cleaning_date}"