from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q


class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Этаж {self.number}"


class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ("single", "Одноместный"),
        ("double", "Двухместный"),
        ("triple", "Трехместный"),
    )

    number = models.PositiveIntegerField(unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, null=False, blank=False)
    price_per_day = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Комната {self.number} ({self.room_type})"

    @classmethod
    def get_free_rooms(cls):
        today = timezone.now().date()
        occupied_rooms = ClientRoom.objects.filter(
            Q(check_out_date__isnull=True) | Q(check_out_date__gte=today)
        ).values_list('room_id', flat=True)
        return cls.objects.exclude(id__in=occupied_rooms)


class Client(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class ClientRoom(models.Model):
    ROOM_CAPACITY = {
        "single": 1,
        "double": 2,
        "triple": 3,
    }

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="stay_history")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="stay_history")
    check_in_date = models.DateField(db_index=True, null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True, db_index=True)
    count_of_clients = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.client} в Комнате {self.room.number} ({self.check_in_date} - {self.check_out_date})"

    def clean(self):
        if self.check_out_date and self.check_out_date < self.check_in_date:
            raise ValidationError("Дата выезда не может быть раньше заезда.")

        max_capacity = self.ROOM_CAPACITY.get(self.room.room_type, 1)
        if self.count_of_clients > max_capacity:
            raise ValidationError(f"Максимальная вместимость комнаты {max_capacity} человека(ов).")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Employee(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class FloorSchedule(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.CharField(
        max_length=9,
        choices=[
            ("Monday", "Понедельник"),
            ("Tuesday", "Вторник"),
            ("Wednesday", "Среда"),
            ("Thursday", "Четверг"),
            ("Friday", "Пятница"),
            ("Saturday", "Суббота"),
            ("Sunday", "Воскресенье"),
        ]
    )

    def __str__(self):
        return f"Уборка на этаже {self.floor.number} в {self.get_day_of_week_display()}"


class CleaningAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_assignments")
    floor_schedule = models.ForeignKey(FloorSchedule, on_delete=models.CASCADE, related_name="cleaning_assignments")

    def __str__(self):
        return f"{self.employee} убирает {self.floor_schedule}"
