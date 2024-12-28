from django.db import models
from django.utils import timezone

from hotel_api.models import Room
from auth_api.models import UserAccount

class Booking(models.Model):
    booking_date = models.DateField(null=False, default=timezone.now)
    from_town = models.CharField(max_length=30)
    check_in_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    full_days = models.IntegerField(default=0)
    state = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30)
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name='bookings')

    def __str__(self):
        return f"Booking from {self.booking_date} by {self.client.firstname} {self.client.lastname}, room {self.room.number}"

