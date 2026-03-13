from django.db import models
from django.conf import settings
from hotels.models import Room

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    stay_start = models.DateField(verbose_name="Начало проживания")
    stay_end = models.DateField(verbose_name="Конец проживания")
    comment = models.TextField(verbose_name="Текст комментария")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг (1-10)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.room} – {self.rating}/10"