from django.db import models
from django.utils.translation import gettext_lazy as _


class BusDriver(models.Model):
    class DriverCategory(models.TextChoices):
        NORMAL_BUS = 'A', _('Обычный автобус')
        ELECTRIC_BUS = 'B', _('Электробус')
        TOURIST_BUS = 'C', _('Туристический автобус')
        CARGO_VEHICLE = 'D', _('Грузовой автобус')

    full_name = models.CharField(max_length=40, verbose_name="ФИО")
    passport = models.CharField(max_length=20, unique=True, verbose_name="Паспортные данные")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы в годах")
    driver_category = models.CharField(max_length=10, choices=DriverCategory.choices, verbose_name="Категория")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")

    def __str__(self):
        return f"{self.full_name} ({self.get_driver_category_display()})"


class Bus(models.Model):
    class BusType(models.TextChoices):
        VERY_SMALL = 'VS', _('Особо малый')
        SMALL = 'S', _('Малый')
        MEDIUM = 'M', _('Средний')
        LARGE = 'L', _('Большой')
        VERY_LARGE = 'VL', _('Особо большой')

    state_num = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    bus_type = models.CharField(max_length=10, choices=BusType.choices)

    def __str__(self):
        return f"{self.state_num} ({self.get_bus_type_display()})"


class Route(models.Model):
    route_num = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.PositiveIntegerField()  # Интервал в минутах
    duration = models.PositiveIntegerField()  # Протяженность в минутах
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Route {self.route_num} is {self.is_active}: {self.start_point} → {self.end_point}"


class WorkSchedule(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        ACCIDENT = 'accident', _('Accident')

    driver = models.ForeignKey(BusDriver, on_delete=models.CASCADE, related_name="schedules")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return f"Schedule: {self.driver.passport} - {self.bus.state_num} on {self.route.route_num}"
