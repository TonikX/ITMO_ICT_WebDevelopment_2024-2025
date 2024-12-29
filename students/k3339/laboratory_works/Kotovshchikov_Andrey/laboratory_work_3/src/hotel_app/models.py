from django.db import models


class Person(models.Model):
    first_name = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        verbose_name="Имя",
    )

    last_name = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        verbose_name="Фамилия",
    )

    patronymic = models.CharField(
        max_length=70,
        null=True,
        blank=True,
        verbose_name="Отчество",
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" + (self.patronymic or "")


class Employee(Person):
    hire_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Дата найма",
    )

    dismissal_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата увольнения",
    )

    floors = models.ManyToManyField(
        "Floor",
        through="Schedule",
        related_name="employees",
    )

    class Meta:
        verbose_name = "Работник гостиницы"
        verbose_name_plural = "Работники гостиницы"
        db_table = "employee"


class Floor(models.Model):
    number = models.SmallIntegerField(
        unique=True,
        null=False,
        blank=False,
        verbose_name="Номер этажа",
    )

    def __str__(self) -> str:
        return str(self.number)

    class Meta:
        verbose_name = "Этаж"
        verbose_name_plural = "Этажи"
        db_table = "floor"


class Schedule(models.Model):
    week_days = (
        ("пн", "понедельник"),
        ("вт", "вторник"),
        ("ср", "среда"),
        ("чт", "четверг"),
        ("пт", "пятница"),
        ("сб", "суббота"),
        ("вс", "воскресенье"),
    )

    week_day = models.CharField(
        max_length=2,
        null=False,
        blank=False,
        verbose_name="День недели",
        choices=week_days,
    )

    employee = models.ForeignKey(
        "Employee",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Работник",
    )

    floor = models.ForeignKey(
        "Floor",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Этаж",
    )

    class Meta:
        db_table = "schedule"


class RoomType(models.Model):
    beds = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Количество кроватей",
    )

    price_per_day = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Цена за день",
    )

    def __str__(self) -> str:
        return f"Номер с количеством кроватей {self.beds}"

    class Meta:
        verbose_name = "Тип гостиничного номера"
        verbose_name_plural = "Типы гостиничых номеров"
        db_table = "room_type"


class Room(models.Model):
    label = models.CharField(
        unique=True,
        max_length=30,
        null=False,
        blank=False,
        verbose_name="Номер на двери",
    )

    phone = models.CharField(
        unique=True,
        max_length=15,
        null=False,
        blank=False,
        verbose_name="Номер телефона",
    )

    floor = models.ForeignKey(
        "Floor",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Этаж",
    )

    room_type = models.ForeignKey(
        "RoomType",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Тип номера",
    )

    def __str__(self) -> str:
        return self.label

    class Meta:
        verbose_name = "Гостиничный номер"
        verbose_name_plural = "Гостиничные номера"
        db_table = "room"


class Booking(models.Model):
    guest = models.ForeignKey(
        "Guest",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="booking",
        verbose_name="Гость",
    )

    room = models.ForeignKey(
        "Room",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="booking",
        verbose_name="Гостиничный номер",
    )

    check_in_date = models.DateField(
        null=False,
        blank=False,
        editable=False,
        auto_now_add=True,
        verbose_name="Дата заселения",
    )

    check_out_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Дата выселения",
    )

    class Meta:
        db_table = "booking"


class Guest(Person):
    passport = models.CharField(
        unique=True,
        max_length=30,
        null=False,
        blank=False,
        verbose_name="Серия и номер паспорта",
    )

    city = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Город",
    )

    rooms = models.ManyToManyField(
        "Room",
        through="Booking",
        related_name="guests",
    )

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"
        db_table = "guest"
