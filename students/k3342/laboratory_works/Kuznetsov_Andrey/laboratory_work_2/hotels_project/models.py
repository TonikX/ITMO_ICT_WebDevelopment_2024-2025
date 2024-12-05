from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta


class Client(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=now)

    def __str__(self):
        return self.username


class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название отеля")
    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="owned_hotels",
        verbose_name="Владелец отеля"
    )
    address = models.CharField(max_length=300, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание", blank=True)
    amenities = models.TextField(verbose_name="Удобства", blank=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип номера")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Отель"
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="rooms",
        verbose_name="Тип номера"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за ночь")
    capacity = models.IntegerField(verbose_name="Вместимость")
    amenities = models.TextField(verbose_name="Удобства", blank=True)

    def __str__(self):
        return f"{self.hotel.name}: {self.room_type}"


class Reservation(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Номер"
    )
    check_in_date = models.DateField(verbose_name="Дата заселения")
    check_out_date = models.DateField(verbose_name="Дата выселения")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_last_month_reservations(cls, hotel_id=None):
        last_month_date = now().date() - timedelta(days=30)
        queryset = cls.objects.filter(check_in_date__gte=last_month_date)
        if hotel_id:
            queryset = queryset.filter(room__hotel__id=hotel_id)
        return queryset

    def __str__(self):
        return f"{self.client} @ {self.room} (created at {self.created_at})"


class Review(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Резервирование"
    )
    comment = models.TextField(verbose_name="Комментарий")
    rating = models.IntegerField(verbose_name="Рейтинг", choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"{self.rating}/10"
