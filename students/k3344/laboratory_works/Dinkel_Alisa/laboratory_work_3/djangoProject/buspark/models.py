from django.db import models
from datetime import date


class BusCategory(models.Model):
    """Тип автобуса с автоматическим определением вместимости"""
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Тип автобуса"
        verbose_name_plural = "Типы автобусов"

    def __str__(self):
        return f"{self.name} ({self.capacity} мест)"


class Bus(models.Model):
    """Автобус с регистрационным номером и типом"""
    registration_number = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(BusCategory, on_delete=models.PROTECT)

    @property
    def capacity(self):
        return self.category.capacity  # Вместимость берётся из категории

    class Meta:
        verbose_name = "Автобус"
        verbose_name_plural = "Автобусы"

    def __str__(self):
        return f"Автобус {self.registration_number} ({self.capacity} мест)"


class Driver(models.Model):
    """Водитель с личными данными и динамическим расчетом зарплаты"""
    passport_number = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=40, verbose_name="ФИО")

    CLASS_I = 'I'
    CLASS_II = 'II'
    CLASS_III = 'III'
    CLASS_CHOICES = [
        (CLASS_I, 'I класс'),
        (CLASS_II, 'II класс'),
        (CLASS_III, 'III класс'),
    ]

    driver_class = models.CharField(max_length=3, choices=CLASS_CHOICES)
    experience = models.PositiveSmallIntegerField(help_text="Стаж работы в годах")

    BASE_SALARY = {
        CLASS_I: 50000,
        CLASS_II: 60000,
        CLASS_III: 70000,
    }
    EXPERIENCE_BONUS = 1000  # Доплата за каждый год стажа

    @property
    def salary(self):
        """Оклад зависит от категории и стажа"""
        base = self.BASE_SALARY.get(self.driver_class, 50000)
        return base + (self.experience * self.EXPERIENCE_BONUS)

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return f"Водитель {self.full_name} ({self.driver_class}, {self.experience} лет стажа, {self.salary} руб.)"


class Route(models.Model):
    """Маршрут с расписанием движения и протяженностью"""
    route_number = models.CharField(max_length=20, unique=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return f"Маршрут {self.route_number}: {self.start_point} - {self.end_point}"


class Shift(models.Model):
    """Рабочая смена водителя с возможностью замены автобуса при поломке"""
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    ACTIVE = 'Active'
    BROKEN_DOWN = 'Breakdown'
    NO_DRIVER = 'No Driver'
    STATUS_CHOICES = [
        (ACTIVE, 'Отработано'),
        (BROKEN_DOWN, 'Поломка автобуса'),
        (NO_DRIVER, 'Нет водителя'),
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ACTIVE)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('driver', 'shift_date', 'start_time', 'end_time')
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    def __str__(self):
        return f"Смена {self.shift_date}: {self.driver} на {self.bus or 'заменён'} ({self.status})"
