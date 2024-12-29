from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

# Модель гостя отеля
class Guest(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guest_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Модель отеля
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

# Модель типа номера
class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

# Модель номера
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    amenities = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.hotel.name} - Room {self.id}'

# Модель бронирования
class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reservation by {self.guest.user.username} for Room {self.room.id}'

# Модель отзыва
class Review(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    stay_period = models.CharField(max_length=50)

    def __str__(self):
        return f'Review by {self.reservation.guest.user.username} - Rating {self.rating}'

# Ассоциативная модель для хранения информации о бронировании
class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)  # Связь с гостем
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Связь с номером
    check_in = models.DateField()  # Дата заезда
    check_out = models.DateField()  # Дата выезда

    def __str__(self):
        return f"Booking: {self.guest.user.username} - {self.room.room_type} from {self.check_in} to {self.check_out}"
