from django.db import models
from django.utils.translation import gettext_lazy as _


class Driver(models.Model):
    class DriverStatus(models.TextChoices):
        ACTIVE = 'На работе', _('На работе')
        WEEKEND = 'Выходной', _('Выходной')
        REST = 'В отпуске', _('В отпуске')
        ILLNESS = 'На больничном', _('На больничном')
        TRIP = 'В командировке', _('В командировке')

    name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    passport = models.CharField(max_length=10, unique=True, verbose_name="Паспортные данные")
    driver_class = models.CharField(max_length=20, verbose_name="Класс водителя")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы (лет)")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оклад")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    status = models.CharField(max_length=30, choices=DriverStatus.choices, verbose_name="Статус")
    routes = models.ManyToManyField('Route', verbose_name="Маршруты", related_name="drivers")

    def __str__(self):
        return f"{self.name} {self.surname} ({self.driver_class})"


class Route(models.Model):
    route_num = models.PositiveIntegerField(verbose_name="Номер маршрута", unique=True)
    start_point = models.CharField(max_length=30, verbose_name="Начальный пункт")
    end_point = models.CharField(max_length=30, verbose_name="Конечный пункт")
    start_time = models.TimeField(verbose_name="Время начала движения")
    end_time = models.TimeField(verbose_name="Время конца движения")
    interval = models.PositiveIntegerField(verbose_name="Интервал движения (мин.)")
    duration = models.PositiveIntegerField(verbose_name="Длительность (мин.)")

    def __str__(self):
        return f"Маршрут {self.route_num}: {self.start_point} - {self.end_point}"


class Bus(models.Model):
    class BusStatus(models.TextChoices):
        AVAILABLE = 'Свободен', _('Свободен')
        IN_REPAIR = 'В ремонте', _('В ремонте')
        UNAVAILABLE = 'Занят', _('Занят')

    registration_num = models.CharField(max_length=20, unique=True, verbose_name="Регистрационный номер")
    type = models.CharField(max_length=30, verbose_name="Тип автобуса")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    status = models.CharField(max_length=30, choices=BusStatus.choices, verbose_name="Статус")

    def __str__(self):
        return f"{self.registration_num} ({self.type})"



class DriverSchedule(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Автобус")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Маршрут")
    work_date = models.DateField(verbose_name="Дата работы")
    shift_start = models.TimeField(verbose_name="Начало смены")
    shift_end = models.TimeField(verbose_name="Конец смены")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["driver", "bus", "route", "work_date"],
                name="unique_schedule_entry"
            )
        ]

    def __str__(self):
        return f"{self.driver.name} on {self.route.route_num} ({self.work_date})"


class BusAssignment(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Автобус")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Маршрут")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)

    def __str__(self):
        return f"{self.bus.registration_num} on {self.route.route_num}"


class Maintenance(models.Model):
    class MaintenanceStatus(models.TextChoices):
        PENDING = 'В процессе', _('В процессе')
        COMPLETED = 'Починен', _('Починен')

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Автобус")
    maintenance_date = models.DateField(verbose_name="Дата обслуживания")
    reason = models.CharField(max_length=30, verbose_name="Причина")
    status = models.CharField(max_length=30, choices=MaintenanceStatus.choices, verbose_name="Статус")

    def __str__(self):
        return f"Maintenance on {self.bus.registration_num} ({self.maintenance_date})"
