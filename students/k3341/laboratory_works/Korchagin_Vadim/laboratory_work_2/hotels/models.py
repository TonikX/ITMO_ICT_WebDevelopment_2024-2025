from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

# Проверка, что дата установлена на будущее
def validate_future_date(value):
    if value < date.today():
        raise ValidationError(
            _('%(value)s is in the past! Please enter a future date.'),
            params={'value': value},
        )

# Модель отеля
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels')
    address = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Модель типа номера (например, "Люкс", "Эконом")
class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Модель номера
class Room(models.Model):
    # Отель, к которому принадлежит номер
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    # Тип номера
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    cost_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    amenities = models.TextField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.name}"

# Модель бронирования
class Booking(models.Model):
    # Возможные статусы бронирования
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    # Пользователь, совершивший бронирование
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    # Номер, который бронируется
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    # Статус бронирования
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Проверка, что дата окончания после даты начала
    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(_('Конечная дата должна быть позже начальной.'))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} in {self.room}"


# Модель отзыва о бронировании
class Review(models.Model):
    # Бронирование, к которому относится отзыв
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews')
    # Рейтинг отзыва
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Рейтинг должен быть минимум 1"),
            MaxValueValidator(10, message="Рейтинг не должен превышать 10")
        ]
    )
    comment = models.TextField()

    # Установка дат проживания из бронирования
    def save(self, *args, **kwargs):
        if self.booking:
            self.start_date = self.booking.start_date
            self.end_date = self.booking.end_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв {self.booking.user.username} для {self.booking.room}"


class Guest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_bookings')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    is_primary_guest = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} находится {self.booking.room}"