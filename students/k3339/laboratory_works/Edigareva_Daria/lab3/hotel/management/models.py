from django.contrib.auth.models import AbstractUser
from django.db import models


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    ]

    number = models.IntegerField(unique=True, verbose_name="Номер комнаты")
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, verbose_name="Тип комнаты")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за сутки")
    phone = models.CharField(max_length=15, verbose_name="Телефон в комнате")
    floor = models.IntegerField(verbose_name="Этаж")

    def __str__(self):
        return f"Комната {self.number} ({self.get_room_type_display()})"


class Client(models.Model):
    passport = models.CharField(max_length=20, unique=True, verbose_name="Паспорт")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="bookings", verbose_name="Клиент")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings", verbose_name="Комната")
    start_date = models.DateField(verbose_name="Дата начала бронирования")
    end_date = models.DateField(verbose_name="Дата окончания бронирования")

    def __str__(self):
        return f"Бронь {self.room} для {self.client}"


class Staff(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="cleaning_schedules",
                              verbose_name="Сотрудник")
    day_of_week = models.CharField(max_length=15, verbose_name="День недели")

    def __str__(self):
        return f"{self.staff} ({self.day_of_week})"


class CleaningConfirmation(models.Model):
    schedule = models.ForeignKey(CleaningSchedule, on_delete=models.CASCADE, related_name="cleanings",
                                 verbose_name="График уборки")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cleaning_confirmations",
                             verbose_name="Комната")
    cleaning_date = models.DateField(verbose_name="Дата уборки")
    status = models.CharField(max_length=50, verbose_name="Статус уборки")

    def __str__(self):
        return f"Уборка {self.room} ({self.cleaning_date})"
