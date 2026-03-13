from django.db import models
from django.conf import settings
from hotels.models import Room

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False, verbose_name="Заселён")
    is_checked_out = models.BooleanField(default=False, verbose_name="Выселен")

    def __str__(self):
        return f"{self.user.username} – {self.room} ({self.check_in} - {self.check_out})"