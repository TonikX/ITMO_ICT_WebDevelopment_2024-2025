from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} profile'

class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_hotels')
    address = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


ROOM_TYPES = [
    ('single', 'Single'),
    ('double', 'Double'),
    ('suite', 'Suite'),
]

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='rooms')

    def __str__(self):
        return f'{self.hotel.name} - {self.number} ({self.get_room_type_display()})'

BOOKING_STATUS = [
    ('reserved', 'Reserved'),
    ('checked_in', 'Checked in'),
    ('checked_out', 'Checked out'),
    ('cancelled', 'Cancelled'),
]

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='reserved')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.room} ({self.check_in} → {self.check_out})'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    stay_from = models.DateField()
    stay_to = models.DateField()
    rating = models.PositiveSmallIntegerField()  # 1-10
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review {self.rating} by {self.user}'