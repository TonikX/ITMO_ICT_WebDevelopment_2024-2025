from django.db import models
from django.db.models import ForeignKey


class RoomType(models.Model):
    room_category = models.CharField(max_length=50, primary_key=True, verbose_name='Категория номера')
    night_cost = models.IntegerField(default=0, verbose_name='Стоимость за ночь')
    guest_count = models.IntegerField(default=2, verbose_name='Количество спальных мест')
    description = models.CharField(max_length=100, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'

    def __str__(self):
        return self.room_category


class Floor(models.Model):
    fix_date = models.DateField(auto_now=True, verbose_name='Дата ремонта')
    clean_date = models.DateField(auto_now=True, verbose_name='Дата уборки')
    rooms_count = models.IntegerField(default=0, verbose_name='Количество номеров')
    cleaner = models.ManyToManyField("staff.Employee", related_name="cleaner", verbose_name='Уборщик')


    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return str(self.id)


class Room(models.Model):
    room_category = models.ForeignKey(RoomType,on_delete=models.CASCADE, verbose_name='Категория номера')
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE, verbose_name='Этаж')
    phone = models.IntegerField(default=0, verbose_name='Телефон')
    is_occupied = models.BooleanField(default=False, verbose_name='Занятость номера')
    is_active = models.BooleanField(default=True, verbose_name='Готовность номера')
    guest_count = models.IntegerField(default=2, verbose_name='Количество гостей')
    description = models.CharField(max_length=100, verbose_name='Описание')

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        return str(self.id)