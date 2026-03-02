from django.conf import settings
from django.db import models
from django.utils import timezone


class Hotel(models.Model):
    name = models.CharField("Название отеля", max_length=200)
    owner = models.CharField("Владелец", max_length=200)
    address = models.CharField("Адрес", max_length=300)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('lux', 'Люкс'),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Отель",
    )
    room_type = models.CharField(
        "Тип номера",
        max_length=50,
        choices=ROOM_TYPE_CHOICES,
    )
    price = models.DecimalField("Стоимость за ночь", max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField("Вместимость")
    facilities = models.TextField("Удобства")

    def __str__(self):
        return f"{self.hotel.name} — {self.get_room_type_display()}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    date_from = models.DateField("Дата заезда")
    date_to = models.DateField("Дата выезда")
    created_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    def __str__(self):
        return f"{self.user} — {self.room}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    stay_from = models.DateField()
    stay_to = models.DateField()
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Отзыв {self.user} ({self.rating}/10)"
