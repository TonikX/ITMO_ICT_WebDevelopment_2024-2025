from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class RoomType(models.Model): # типы номеров
    name = models.CharField(max_length=50, unique=True, verbose_name="Название типа")
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество мест"
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за сутки"
    )

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"

    def __str__(self):
        return f"{self.name} ({self.capacity} мест)"


class Room(models.Model): # номер
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name="rooms",
        verbose_name="Тип номера"
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Номер в эксплуатации"
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

    def __str__(self):
        return f"№{self.number} — {self.room_type}"


class Guest(models.Model): # класс гостя с персональными данными
    passport = models.CharField(max_length=20, unique=True, verbose_name="Паспорт")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город прибытия")

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.passport})"

class Booking(models.Model): # Бронь: заселение/выселение
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='bookings', verbose_name="Гость")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings', verbose_name="Номер")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(null=True, blank=True, verbose_name="Дата выезда")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Заселение"
        verbose_name_plural = "Заселения"
        # ordering = ['-check_in']

    def __str__(self):
        return f"{self.guest} → №{self.room.number} ({self.check_in})"

    @property
    def is_active(self):
        """Сейчас живёт в номере?"""
        today = timezone.now().date()
        return self.check_in <= today and (self.check_out is None or self.check_out >= today)


class Employee(models.Model): # сотрудник
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    is_active = models.BooleanField(default=True, verbose_name="Работает")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningAssignment(models.Model):
    """Расписание уборки: сотрудник → этаж → день недели"""
    DAYS_OF_WEEK = (
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cleaning_assignments', verbose_name="Сотрудник")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, verbose_name="День недели")

    class Meta:
        verbose_name = "Назначение уборки"
        verbose_name_plural = "Назначения уборки"
        unique_together = [['employee', 'floor', 'day_of_week']]

    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK)[self.day_of_week]
        return f"{self.employee} — этаж {self.floor} — {day_name}"