from django.db import models

from django.db import models
from django.contrib.auth.models import User

from rooms.models import Room
from booking import Booking

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    is_staff_member = models.BooleanField(default=False, verbose_name='Сотрудник отеля')
    passport_number = models.CharField(max_length=20, unique=True, verbose_name='Номер паспорта')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    city = models.CharField(max_length=100, verbose_name='Город')
    bookings = models.ManyToManyField("booking.Booking", related_name="user_profile", verbose_name='Брони')

    def __str__(self):
        return self.user.username