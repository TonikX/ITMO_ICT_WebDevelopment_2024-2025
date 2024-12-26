from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Отель «{self.name}»"


class RoomType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    room_services = models.TextField()

    def __str__(self):
        return f"Номер «{self.room_type}» в отеле «{self.hotel.name}», цена: {self.price} ₽"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date <= timezone.now().date():
            raise ValidationError('Дата начала должна быть позже сегодняшнего дня.')

        if self.start_date >= self.end_date:
            raise ValidationError('Дата начала должна быть раньше даты окончания.')

    def __str__(self):
        return f"Бронирование: {self.user.username}, {self.room.room_type} с {self.start_date} по {self.end_date}"


class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"Отзыв от {self.reservation.user.username} на {self.reservation.room.room_type} - Оценка: {self.rate}/10"
