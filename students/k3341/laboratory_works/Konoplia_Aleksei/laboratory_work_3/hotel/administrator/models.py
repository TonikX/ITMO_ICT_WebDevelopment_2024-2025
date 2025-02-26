from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'
    TRIPLE = 'TRIPLE'

    ROOM_TYPE_CHOICES = [
        (SINGLE, 'Одноместный'),
        (DOUBLE, 'Двухместный'),
        (TRIPLE, 'Трехместный'),
    ]

    room_id = models.AutoField(primary_key=True)
    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE_CHOICES,
        verbose_name='Тип номера'
    )
    cost_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость за день'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона'
    )
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    is_available = models.BooleanField(default=True, verbose_name='Свободен')

    def __str__(self):
        return f"Номер: {self.room_id} ({self.get_room_type_display()}, Этаж: {self.floor})"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.AutoField(primary_key=True)
    passport_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер паспорта'
    )
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Отчество'
    )
    city_of_origin = models.CharField(
        max_length=100,
        verbose_name='Город прибытия'
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}, Паспорт: {self.passport_number}"

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Отчество'
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Stay(models.Model):
    stay_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='stays',
        verbose_name='Клиент'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='stays',
        verbose_name='Номер'
    )
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')

    

    def __str__(self):
        return f"Проживание {self.client} в номере {self.room}"

class CleaningSchedule(models.Model):
    cleaning_schedule_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='cleaning_schedules',
        verbose_name='Сотрудник'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cleaning_schedules',
        verbose_name='Номер'
    )
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    time_and_day_of_week = models.CharField(
        max_length=50,
        verbose_name='Время и день недели'
    )

    def __str__(self):
        return f"Расписание уборки {self.staff} на этаже {self.floor}"

class CleaningExecution(models.Model):
    cleaning_execution_id = models.AutoField(primary_key=True)
    cleaning_schedule = models.ForeignKey(
        CleaningSchedule,
        on_delete=models.CASCADE,
        related_name='executions',
        verbose_name='Расписание уборки'
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='cleaning_executions',
        verbose_name='Сотрудник'
    )
    time_and_day_of_week = models.CharField(
        max_length=50,
        verbose_name='Время и день недели'
    )
    floor = models.PositiveIntegerField(verbose_name='Этаж')
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cleaning_executions',
        verbose_name='Номер'
    )

    def __str__(self):
        return f"Уборка {self.staff} в {self.time_and_day_of_week}"