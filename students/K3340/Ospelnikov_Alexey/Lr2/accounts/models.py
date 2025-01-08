from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    is_staff_member = models.BooleanField(default=False, verbose_name='Сотрудник отеля')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username