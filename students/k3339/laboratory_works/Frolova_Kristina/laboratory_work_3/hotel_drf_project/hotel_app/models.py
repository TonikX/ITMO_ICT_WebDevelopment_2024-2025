from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models


class Room(models.Model):
    room_types = (
        ('s', 'single'),
        ('d', 'double'),
        ('t', 'triple'),
    )

    type = models.CharField(max_length=1, choices=room_types, verbose_name='Тип номера')
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона комнаты')
    cost = models.IntegerField(verbose_name='Стоимость проживания за сутки', validators=[MinValueValidator(1000), MaxValueValidator(100000)])
    floor = models.IntegerField(verbose_name='Этаж', validators=[MinValueValidator(1), MaxValueValidator(5)])


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    passport_number = models.CharField(max_length=10, verbose_name='Номер паспорта')
    city_from = models.CharField(max_length=50, verbose_name='Город')


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Администратор')
    arrival_date = models.DateField(verbose_name='Дата заселения')
    departure_date = models.DateField(verbose_name='Дата выселения')


class Employee(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    passport_number = models.CharField(max_length=10, verbose_name='Номер паспорта')


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

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    day_of_week = models.CharField(max_length=3, choices=days_of_week, verbose_name='День недели')
    floor = models.IntegerField(verbose_name='Этаж', validators=[MinValueValidator(1), MaxValueValidator(5)])
