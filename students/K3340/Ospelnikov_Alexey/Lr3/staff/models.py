from django.db import models

from rooms.models import Floor


class Employee(models.Model):
    passport = models.CharField(max_length=50, verbose_name='Паспорт')
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    employee_date = models.DateField(auto_now_add=True, verbose_name='Дата трудоустройства')
    fire_date = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')
    salary = models.IntegerField(verbose_name='Оклад')
    rank = models.CharField(max_length=50, verbose_name='Должность')
    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.full_name


class RoomClean(models.Model):
    complaints = models.CharField(max_length=50, verbose_name='Жалобы')
    clean_mark = models.IntegerField(default=5, verbose_name='Оценка')
    clean_date = models.DateField(auto_now_add=True, verbose_name='Дата уборки')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    worker_id = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Уборщик')

    class Meta:
        verbose_name = 'Уборка этажа'
        verbose_name_plural = 'Уборка этажей'

    def __str__(self):
        return str(self.worker_id)