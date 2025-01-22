from django.db import models

LICENSE_TYPES = [
    ('A', 'Мотоциклы'),
    ('A1', 'Легкие мотоциклы'),
    ('B', 'Легковые автомобили'),
    ('B1', 'Трициклы и квадрициклы'),
    ('C', 'Грузовые автомобили'),
    ('C1', 'Небольшие грузовые автомобили (3.5-7.5 тонн)'),
    ('D', 'Автобусы'),
    ('D1', 'Небольшие автобусы (8-16 пассажиров)'),
    ('BE', 'Легковые автомобили с прицепами'),
    ('CE', 'Грузовые автомобили с прицепами'),
    ('DE', 'Автобусы с прицепами'),
    ('M', 'Мопеды и скутеры'),
    ('Tm', 'Трамваи'),
    ('Tb', 'Троллейбусы'),
]


class CarOwner(models.Model):
    last_name = models.CharField(max_length=128, verbose_name='Фамилия')
    first_name = models.CharField(max_length=128, verbose_name='Имя')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Car(models.Model):
    license_plate = models.CharField(max_length=15, verbose_name='Гос. номер')
    brand = models.CharField(max_length=64, verbose_name='Марка')
    model = models.CharField(max_length=64, verbose_name='Модель')
    color = models.CharField(max_length=32, default='Неизвестно', blank=True, verbose_name='Цвет')
    car_owner = models.ManyToManyField(CarOwner, through='Ownership', related_name='cars')

    def __str__(self):
        return f'{self.brand} {self.model} ({self.license_plate})'


class Ownership(models.Model):
    car_owner = models.ForeignKey(
        CarOwner,
        on_delete=models.SET_NULL,  # связь необязательная
        null=True,
        blank=True,
        verbose_name='Владелец',
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,  # связь необязательная
        null=True,
        blank=True,
        verbose_name='Автомобиль',
    )
    start_date = models.DateField(verbose_name='Дата начала владения')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания владения')

    def __str__(self):
        return f'{self.car_owner} -> {self.car}'


class DriverLicense(models.Model):
    """
    Таблица "Водительское удостоверение"
    """

    car_owner = models.OneToOneField(
        CarOwner,
        on_delete=models.CASCADE,  # Обязательная связь с автовладельцем
        verbose_name='Владелец',
        related_name='driver_license',
    )
    license_number = models.CharField(max_length=10, verbose_name='Номер удостоверения')
    license_type = models.CharField(
        max_length=4,
        choices=LICENSE_TYPES,
        verbose_name='Категория',
    )
    issue_date = models.DateField(verbose_name='Дата выдачи')

    def __str__(self):
        return f'{self.license_number} ({self.get_license_type_display()}) - {self.car_owner}'
