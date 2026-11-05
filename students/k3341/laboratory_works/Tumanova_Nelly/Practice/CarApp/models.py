from django.db import models

# Create your models here.
class Car(models.Model):
    number_plate = models.CharField(max_length=15)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)


class CarOwner(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class LicenseType(models.TextChoices):
    M = 'M', 'Категория M – Мопеды, скутеры и легкие квадрициклы'
    A = 'A', 'Категория A – Мотоциклы любых видов, включая модели с коляской'
    A1 = 'A1', 'Категория A1 – Легкие мотоциклы с объемом двигателя до 125 см³ и мощностью до 11 кВт'
    B = 'B', 'Категория B – Легковые автомобили с разрешенной максимальной массой до 3,5 тонн и числом пассажирских мест не более 8'
    B1 = 'B1', 'Категория B1 – Трициклы и квадрициклы'
    BE = 'BE', 'Категория BE – Легковые автомобили (категории B) с прицепом массой более 750 кг'
    C = 'C', 'Категория C – Грузовые автомобили с разрешенной максимальной массой свыше 3,5 тонн'
    C1 = 'C1', 'Категория C1 – Средние грузовые автомобили массой от 3,5 до 7,5 тонн'
    CE = 'CE', 'Категория CE – Грузовые автомобили (категории C) с прицепом массой более 750 кг'
    C1E = 'C1E', 'Категория C1E – Средние грузовики (категории C1) с прицепом тяжелее 750 кг, если общая масса состава до 12 тонн'
    D = 'D', 'Категория D – Автобусы для перевозки пассажиров, имеющие более 8 сидячих мест'
    D1 = 'D1', 'Категория D1 – Малые автобусы с числом сидячих мест от 8 до 16'
    DE = 'DE', 'Категория DE – Автобусы (категории D) с прицепом массой более 750 кг, включая сочлененные автобусы'
    D1E = 'D1E', 'Категория D1E – Малые автобусы (категории D1) с прицепом тяжелее 750 кг для непассажирских перевозок до 12 тонн общей массы'
    TM = 'Tm', 'Категория Tm – Трамваи'
    TB = 'Tb', 'Категория Tb – Троллейбусы'


class License(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=LicenseType.choices)
    issue_date = models.DateField()


