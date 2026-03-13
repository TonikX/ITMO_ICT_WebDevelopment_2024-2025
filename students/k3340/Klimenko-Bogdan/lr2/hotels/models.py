from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название отеля")
    owner = models.CharField(max_length=200, verbose_name="Владелец")
    address = models.TextField(verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100, verbose_name="Тип номера")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    amenities = models.TextField(verbose_name="Удобства", blank=True)
    def __str__(self):
        return f"{self.hotel.name} – {self.room_type}"