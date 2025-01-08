from django.db import models
from django.conf import settings
from hotels.models import Room


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews', verbose_name='Номер')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.TextField(verbose_name='Комментарий')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name='Рейтинг')
    stay_start = models.DateField(verbose_name='Начало проживания')
    stay_end = models.DateField(verbose_name='Конец проживания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.name} на {self.room}"