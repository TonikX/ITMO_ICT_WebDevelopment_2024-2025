from django.db import models
from django.core.validators import MinValueValidator


class Sport(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    type = models.CharField(max_length=1, choices=(('t', 'team'), ('i', 'individual')), verbose_name='Тип')


class Coach(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя тренера')
    last_name = models.TextField(max_length=50, verbose_name='Фамилия тренера')
    middle_name = models.TextField(max_length=50, verbose_name='Отчество тренера')
    gender = models.CharField(max_length=1, choices=(('m', 'male'), ('f', 'female')), verbose_name='Пол тренера')
    date_of_birth = models.DateField(verbose_name='Дата рождения тренера')
    qualification = models.TextField(max_length=100, verbose_name='Квалификация')
    experience = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Опыт работы')


class Sportsman(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя спортсмена')
    last_name = models.TextField(max_length=50, verbose_name='Фамилия спортсмена')
    middle_name = models.TextField(max_length=50, verbose_name='Отчество спортсмена')
    gender = models.CharField(max_length=1, choices=(('m', 'male'), ('f', 'female')), verbose_name='Пол спортсмена')
    date_of_birth = models.DateField(verbose_name='Дата рождения спортсмена')
    phone_number = models.CharField(max_length=11, verbose_name='Телефон')
    email = models.CharField(max_length=50, verbose_name='Почта')
    registration_date = models.DateField(verbose_name='Дата регистрации')


class SportHall(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название зала')
    address = models.CharField(max_length=50, verbose_name='Адрес')
    sport = models.ManyToManyField('Sport', verbose_name='Вид спорта')


class SportSection(models.Model):
    title = models.TextField(max_length=50, verbose_name='Наименование')
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE, verbose_name='Вид спорта')
    description = models.TextField(max_length=100, verbose_name='Описание')
    capacity = models.IntegerField(verbose_name='Вместимость группы')
    sportsmen = models.ManyToManyField('Sportsman', verbose_name='Спортсмены')


class SportSectionCoaches(models.Model):
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE, verbose_name='Тренер')
    section = models.ForeignKey('SportSection', on_delete=models.CASCADE, verbose_name='Секция')
    start = models.DateField(verbose_name='Принят на должность')
    end = models.DateField(null=True, blank=True, verbose_name='Уволен с должности')


class Schedule(models.Model):
    sport_section = models.ForeignKey('SportSection',  on_delete=models.CASCADE, verbose_name='Секция')
    sport_hall = models.ForeignKey('SportHall',  on_delete=models.CASCADE, verbose_name='Зал')
    weekday = models.TextField(max_length=15, choices=(
        ("Понедельник", "Понедельник"),
        ("Вторник", "Вторник"),
        ("Среда", "Среда"),
        ("Четверг", "Четверг"),
        ("Пятница", "Пятница"),
        ("Суббота", "Суббота"),
        ("Воскресенье", "Воскресенье"),
    ), verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Начало')
    end_time = models.TimeField(verbose_name='Конец')
