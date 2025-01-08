from django.db import models
from django.conf import settings
from hotels.models import Room


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings',
                             verbose_name='Пользователь')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')
    is_active = models.BooleanField(default=True, verbose_name='Активная бронь')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Бронь {self.user.username} на {self.room}"