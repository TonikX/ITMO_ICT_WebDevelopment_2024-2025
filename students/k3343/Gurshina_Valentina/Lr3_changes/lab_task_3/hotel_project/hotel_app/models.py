from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models


class Room(models.Model):
    room_types = (
        ('s', 'single'),
        ('d', 'double'),
        ('t', 'triple'),
    )

    type = models.CharField(max_length=1, choices=room_types, verbose_name='Вид номера')
    phone_number = models.CharField(max_length=11, verbose_name='Контактный номер комнаты')
    cost = models.IntegerField(verbose_name='Стоимость проживания (в сутки)', validators=[MinValueValidator(25000), MaxValueValidator(100000000)])
    floor = models.IntegerField(verbose_name='Этаж', validators=[MinValueValidator(1), MaxValueValidator(25)])


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    passport_number = models.CharField(max_length=10, verbose_name='Данные паспорта')
    city_from = models.CharField(max_length=50, verbose_name='Город проживания')


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Администратор гостиницы')
    arrival_date = models.DateField(verbose_name='Дата заселения')
    departure_date = models.DateField(verbose_name='Дата выселения')


class Employee(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    passport_number = models.CharField(max_length=10, verbose_name='Данные паспорта')


class EmployeeSchedule(models.Model):
    days_of_week = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Работник')
    day_of_week = models.CharField(max_length=3, choices=days_of_week, verbose_name='День недели')
    floor = models.IntegerField(verbose_name='Этаж', validators=[MinValueValidator(1), MaxValueValidator(25)])
