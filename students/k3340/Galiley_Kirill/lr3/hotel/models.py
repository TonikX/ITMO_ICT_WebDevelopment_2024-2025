from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, Count, Q
from datetime import date, timedelta
from django.utils import timezone

class RoomType(models.TextChoices):
    SINGLE = 'single', 'Одноместный'
    DOUBLE = 'double', 'Двухместный'
    TRIPLE = 'triple', 'Трёхместный'

class WeekDay(models.TextChoices):
    MON = 'mon', 'Понедельник'
    TUE = 'tue', 'Вторник'
    WED = 'wed', 'Среда'
    THU = 'thu', 'Четверг'
    FRI = 'fri', 'Пятница'
    SAT = 'sat', 'Суббота'
    SUN = 'sun', 'Воскресенье'

class Room(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name='Номер комнаты')
    type = models.CharField(max_length=10, choices=RoomType.choices, verbose_name='Тип')
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за сутки')

    @property
    def is_free(self):
        today = date.today()
        return not Stay.objects.filter(room=self, check_in__lte=today, check_out__gt=today).exists()

    class Meta:
        ordering = ['number']
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

class Client(models.Model):
    passport = models.CharField(max_length=20, unique=True, verbose_name='Паспорт')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    city = models.CharField(max_length=100, verbose_name='Город')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Stay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    check_in = models.DateField(verbose_name='Дата заселения')
    check_out = models.DateField(verbose_name='Дата выселения')

    class Meta:
        unique_together = ['room', 'check_in']
        verbose_name = 'Проживание'
        verbose_name_plural = 'Проживания'

class Staff(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    class Meta:
        verbose_name = 'Служащий'
        verbose_name_plural = 'Служащие'

class CleaningSchedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Служащий')
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    day = models.CharField(max_length=3, choices=WeekDay.choices, verbose_name='День недели')

    class Meta:
        unique_together = ['staff', 'floor', 'day']
        verbose_name = 'Расписание уборки'
        verbose_name_plural = 'Расписания уборки'
