from django.db import models

from accounts.models import UserProfile
from rooms.models import Room


class Booking(models.Model):
    book_date = models.DateField(auto_now_add=True, verbose_name='Дата брони')
    prepayment = models.IntegerField(verbose_name='Предоплата')
    night_count = models.IntegerField(default=1, verbose_name='Количество ночей')
    guest_count = models.IntegerField(default=1, verbose_name='Количество гостей')
    client_preference = models.CharField(max_length=50, verbose_name='Предпочтения клиента')
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    guest_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Гость')


    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
    def __str__(self):
        return self.guest_id.first_name