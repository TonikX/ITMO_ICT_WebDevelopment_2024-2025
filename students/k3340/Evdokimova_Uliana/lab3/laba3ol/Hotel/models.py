from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email_address', unique=True, max_length=64)
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    patronymic = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=15, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='user_account_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_account_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone', 'birth_date']


class Room(models.Model):
    number = models.CharField(unique=True, max_length=4)
    area = models.IntegerField(null=False)
    is_occupied = models.BooleanField(default=False)
    is_cleaned = models.BooleanField(default=True)
    floor = models.IntegerField(null=False)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, null=False, related_name='rooms')

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(number__regex=r'\d{3,4}'), name='number_constraint'),
            models.CheckConstraint(condition=models.Q(floor__gte=0), name='floor_constraint'),
        ]

    def __str__(self):
        return f"room {self.number}, {self.area} sq meters, is_occupied: {self.is_occupied}"


class RoomType(models.Model):
    name = models.CharField(unique=True, max_length=30, null=False)
    places = models.IntegerField(null=False)
    description = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(places__lte=4), name='places <= 4'),
            models.CheckConstraint(condition=models.Q(places__gte=1), name='places >= 1')
        ]

    def __str__(self):
        return "room type:" + self.name


class RoomTypePrice(models.Model):
    day_price = models.IntegerField(null=False)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField()
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, null=False, related_name='prices')

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(day_price__gt=0), name='price > 0'),
        ]


class Employee(models.Model):
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    patronymic = models.CharField(max_length=30)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=15, null=False)

    def __str__(self):
        return f'Employee {self.firstname} {self.lastname}'


class Position(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField()

    def __str__(self):
        return f'Position {self.name} : {self.description}'


class SalaryHistory(models.Model):
    salary = models.IntegerField(null=False)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=False, related_name='salary_history')

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(salary__gt=0), name='salary > 0'),
        ]


class Contract(models.Model):
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField(null=True)
    working_status = models.CharField(max_length=30, null=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, related_name='contracts')
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=False, related_name='contracts')

    def __str__(self):
        return f'Contract from {self.start_date}. Employee {self.employee.firstname} {self.position.name}'


class WorkSchedule(models.Model):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=True)
    is_done = models.BooleanField(default=False)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, null=False, related_name='work_schedule')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name='work_schedule')

    def __str__(self):
        return f'Work schedule from {self.start_time} to {self.end_time} room {self.room.number}'


class Booking(models.Model):
    booking_date = models.DateField(null=False, default=timezone.now)
    from_town = models.CharField(max_length=30)
    check_in_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    full_days = models.IntegerField(default=0)
    state = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30)
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name='bookings')

    def __str__(self):
        return f"Booking from {self.booking_date} by {self.client.firstname} {self.client.lastname}, room {self.room.number}"
