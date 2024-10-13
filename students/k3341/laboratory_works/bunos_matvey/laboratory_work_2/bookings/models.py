from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField('Название отеля', max_length=255)
    owner = models.CharField('Владелец отеля', max_length=255)
    address = models.TextField('Адрес')
    description = models.TextField('Описание')
    amenities = models.TextField('Удобства')

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField('Название типа номера', max_length=100)
    capacity = models.IntegerField('Вместимость')
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)
    amenities = models.TextField('Удобства')

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='rooms', on_delete=models.CASCADE)
    number = models.CharField('Номер комнаты', max_length=10)

    def __str__(self):
        return f"Комната {self.number} ({self.room_type.name})"


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in = models.DateField('Дата заезда')
    check_out = models.DateField('Дата выезда')
    is_checked_in = models.BooleanField('Заселен', default=False)
    is_checked_out = models.BooleanField('Выселен', default=False)

    def __str__(self):
        return f"Бронь {self.user.username} - {self.room}"


class Review(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField('Рейтинг', choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.reservation.user.username} - {self.reservation.room}"
