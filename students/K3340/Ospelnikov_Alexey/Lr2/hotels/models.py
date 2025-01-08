from django.db import models
from django.conf import settings


class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название отеля')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_hotels',
                              verbose_name='Владелец')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип номера')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms', verbose_name='Отель')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    capacity = models.IntegerField(verbose_name='Вместимость')
    amenities = models.TextField(blank=True, verbose_name='Удобства')

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        return f"{self.room_type.name} ({self.hotel.name})"