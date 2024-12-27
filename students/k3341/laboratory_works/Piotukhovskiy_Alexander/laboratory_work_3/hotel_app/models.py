from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название типа номера')
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество мест')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    has_wifi = models.BooleanField(default=False, verbose_name='Бесплатный Wi-Fi')
    has_tea_station = models.BooleanField(default=False, verbose_name='Чайная станция')
    has_coffee_machine = models.BooleanField(default=False, verbose_name='Кофемашина')
    has_iron_board = models.BooleanField(default=False, verbose_name='Утюг и гладильная доска')
    has_safe = models.BooleanField(default=False, verbose_name='Сейф в номере')
    has_hair_dryer = models.BooleanField(default=False, verbose_name='Фен')
    has_tv = models.BooleanField(default=False, verbose_name='Телевизор с плоским экраном')
    has_air_conditioning = models.BooleanField(default=False, verbose_name='Система кондиционирования')
    has_bathrobe_slippers = models.BooleanField(default=False, verbose_name='Халат и тапочки')
    has_balcony = models.BooleanField(default=False, verbose_name='Балкон')


class RoomPriceHistory(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    start_date = models.DateField(verbose_name='Начало действия цены')
    end_date = models.DateField(null=True, blank=True, verbose_name='Конец действия цены')
    price = models.PositiveIntegerField(verbose_name='Стоимость за сутки')


class Room(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Свободен'),
        ('OCCUPIED', 'Занят'),
        ('REQUIRES_CLEANING', 'Требуется уборка'),
        ('CLEANING_IN_PROGRESS', 'Уборка в процессе'),
        ('MAINTENANCE', 'На обслуживании'),
    ]

    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип комнаты')
    status = models.CharField(max_length=len(max(STATUS_CHOICES, key=lambda x: len(x[0]))[0]), choices=STATUS_CHOICES, default='AVAILABLE', verbose_name='Статус комнаты')
    phone = models.CharField(max_length=11, verbose_name='Телефон в номере')


class Client(models.Model):
    passport_number = models.CharField(max_length=10, unique=True, verbose_name='Номер паспорта')
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    city_from = models.CharField(max_length=50, verbose_name='Город')


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('BOOKED', 'Забронирован'),
        ('CONFIRMED', 'Подтвержден'),
        ('CHECKED_IN', 'Заселен'),
        ('CHECKED_OUT', 'Выселен'),
        ('CANCELLED', 'Отменен')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PREPAID', 'Предоплата'),
        ('PAID', 'Оплачен'),
        ('UNPAID', 'Не оплачен'),
        ('REFUNDED', 'Возврат')
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Администратор', related_name="reservations_created")
    booking_date = models.DateField(default=timezone.now, verbose_name='Дата бронирования')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Обновивший администратор", related_name="reservations_updated")
    last_updated_date = models.DateTimeField(default=timezone.now, verbose_name="Дата последнего обновления")

    arrival_date = models.DateField(verbose_name='Дата заселения')
    departure_date = models.DateField(verbose_name='Дата выселения')
    status = models.CharField(max_length=len(max(STATUS_CHOICES, key=lambda x: len(x[0]))[0]), choices=STATUS_CHOICES, default='BOOKED', verbose_name='Статус состояния')
    payment_status = models.CharField(max_length=len(max(PAYMENT_STATUS_CHOICES, key=lambda x: len(x[0]))[0]), choices=PAYMENT_STATUS_CHOICES, default='UNPAID', verbose_name='Статус оплаты')
    price_at_booking = models.PositiveIntegerField(verbose_name='Стоимость при бронировании')
    final_price = models.PositiveIntegerField(verbose_name='Стоимость при бронировании')


class EmployeePosition(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название должности')
    salary = models.PositiveIntegerField(verbose_name='Оклад')


class EmploymentContract(models.Model):
    CONTRACT_TYPE_CHOICES = [
        ('FIXED_TERM', 'Срочный'),
        ('PERMANENT', 'Бессрочный'),
        ('CIVIL_CONTRACT', 'ГПХ')
    ]

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name='Сотрудник')
    position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE, verbose_name='Должность')
    contract_type = models.CharField(max_length=len(max(CONTRACT_TYPE_CHOICES, key=lambda x: len(x[0]))[0]), choices=CONTRACT_TYPE_CHOICES, verbose_name='Тип контракта')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    termination_date = models.DateField(null=True, blank=True, verbose_name='Дата расторжения')
    is_active = models.BooleanField(default=True, verbose_name='Активный контракт')


    def terminate_contract(self, termination_date=None):
        if termination_date is None:
            termination_date = timezone.now()
        elif termination_date > timezone.now():
            raise ValidationError("Дата расторжения контракта не может быть в будущем.")
        self.termination_date = termination_date
        self.is_active = False
        self.save()


class Employee(models.Model):
    passport_number = models.CharField(max_length=10, unique=True, verbose_name='Номер паспорта')
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")


class CleaningSchedule(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Ожидается'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершена')
    ]

    cleaner = models.ForeignKey(EmploymentContract, on_delete=models.CASCADE, verbose_name='Сотрудник')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    cleaning_date = models.DateField(verbose_name='Дата уборки')
    status = models.CharField(max_length=len(max(STATUS_CHOICES, key=lambda x: len(x[0]))[0]), choices=STATUS_CHOICES, default='PENDING', verbose_name='Статус уборки')
