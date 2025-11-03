from __future__ import annotations
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Amenity(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название удобства",
        help_text="Укажите название удобства (например, Wi-Fi, Кондиционер)"
    )

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"
        ordering = ['name']

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название отеля",
        help_text="Укажите полное название отеля"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_hotels',
        verbose_name="Владелец",
        help_text="Владелец или управляющий отеля"
    )
    address = models.CharField(
        max_length=300,
        verbose_name="Адрес",
        help_text="Полный адрес отеля"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание отеля"
    )
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name='hotels',
        verbose_name="Удобства",
        help_text="Выберите все доступные удобства в отеле"
    )

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner']),
        ]

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип номера",
        help_text="Укажите тип номера (например, Люкс, Стандарт)"
    )

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"
        ordering = ['name']

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Отель",
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name='rooms',
        verbose_name="Тип номера",
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за ночь",
        help_text="Стоимость проживания за одну ночь"
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Вместимость",
        help_text="Максимальное количество гостей"
    )
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name='rooms',
        verbose_name="Удобства",
        help_text="Выберите доступные удобства в номере"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Отключите, если номер временно недоступен для бронирования"
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        unique_together = ('hotel', 'id')
        ordering = ['hotel__name', 'id']
        indexes = [
            models.Index(fields=['hotel', 'is_active']),
            models.Index(fields=['price_per_night']),
        ]

    def __str__(self):
        return f"{self.hotel.name} • Номер {self.id}"

    def get_price_display(self):
        """Возвращает отформатированную цену за ночь"""
        return f"{self.price_per_night:,.2f} ₽"

class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ожидает'
        CONFIRMED = 'CONFIRMED', 'Подтверждено'
        CHECKED_IN = 'CHECKED_IN', 'Заселен'
        CHECKED_OUT = 'CHECKED_OUT', 'Выселен'
        CANCELLED = 'CANCELLED', 'Отменено'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Номер"
    )
    check_in = models.DateField(
        verbose_name="Дата заезда",
        help_text="Дата начала проживания"
    )
    check_out = models.DateField(
        verbose_name="Дата выезда",
        help_text="Дата окончания проживания"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
        help_text="Текущий статус бронирования"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'check_in', 'check_out']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'check_in']),
        ]

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError('Дата выезда должна быть позже даты заезда')
        
        # Проверка пересечения броней этой комнаты
        qs = Reservation.objects.filter(room=self.room).exclude(pk=self.pk)
        overlap = qs.filter(
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
            status__in=[self.Status.PENDING, self.Status.CONFIRMED, self.Status.CHECKED_IN]
        ).exists()
        if overlap and self.status != self.Status.CANCELLED:
            raise ValidationError('На выбранные даты уже есть бронирование этой комнаты')

    def can_be_edited(self):
        """Проверяет, можно ли редактировать бронирование"""
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]

    def can_be_cancelled(self):
        """Проверяет, можно ли отменить бронирование"""
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]

    def get_duration(self):
        """Возвращает продолжительность проживания в днях"""
        return (self.check_out - self.check_in).days

    def get_total_price(self):
        """Возвращает полную стоимость проживания"""
        return self.room.price_per_night * self.get_duration()

    def __str__(self):
        return f"{self.user} → {self.room} [{self.check_in}..{self.check_out}] {self.get_status_display()}"

from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Номер"
    )
    stay_from = models.DateField(
        verbose_name="Дата заезда",
        help_text="Дата начала проживания"
    )
    stay_to = models.DateField(
        verbose_name="Дата выезда",
        help_text="Дата окончания проживания"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть меньше 1"),
            MaxValueValidator(10, message="Рейтинг не может быть больше 10")
        ],
        verbose_name="Оценка",
        help_text="Оцените номер от 1 до 10"
    )
    text = models.TextField(
        verbose_name="Отзыв",
        help_text="Поделитесь своими впечатлениями о проживании"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'rating']),
            models.Index(fields=['user', 'room']),
        ]

    def clean(self):
        if self.stay_from >= self.stay_to:
            raise ValidationError('Период проживания указан некорректно')
        
        # Проверить, что у пользователя была бронь этой комнаты, пересекающаяся с периодом отзыва
        had_stay = Reservation.objects.filter(
            user=self.user,
            room=self.room,
            check_in__lt=self.stay_to,
            check_out__gt=self.stay_from,
            status__in=[
                Reservation.Status.CONFIRMED,
                Reservation.Status.CHECKED_IN,
                Reservation.Status.CHECKED_OUT
            ]
        ).exists()
        if not had_stay:
            raise ValidationError('Отзыв можно оставить только после проживания в номере')

    def get_stay_duration(self):
        """Возвращает продолжительность проживания в днях"""
        return (self.stay_to - self.stay_from).days

    def __str__(self):
        return f"{self.room} • {self.rating}/10"