from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class RacingUser(AbstractUser):
    bio = models.TextField(blank=True, verbose_name="Биография")
    experience_years = models.IntegerField(
        default=0,
        verbose_name="Опыт вождения (лет)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название команды")
    description = models.TextField(blank=True, verbose_name="Описание команды")
    founded_date = models.DateField(verbose_name="Дата основания")
    country = models.CharField(max_length=50, verbose_name="Страна")
    logo = models.ImageField(upload_to='teams/', blank=True, null=True, verbose_name="Логотип")

    def __str__(self):
        return self.name


class Car(models.Model):
    CAR_CLASSES = [
        ('F1', 'Формула-1'),
        ('GT', 'Гран-туризмо'),
        ('Rally', 'Ралли'),
        ('Endurance', 'Эндуранс'),
        ('Drift', 'Дрифт'),
    ]

    model = models.CharField(max_length=100, verbose_name="Модель автомобиля")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    car_class = models.CharField(max_length=20, choices=CAR_CLASSES, verbose_name="Класс автомобиля")
    engine = models.CharField(max_length=100, verbose_name="Двигатель")
    horsepower = models.IntegerField(verbose_name="Лошадиные силы")
    description = models.TextField(blank=True, verbose_name="Описание автомобиля")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Фото автомобиля")

    def __str__(self):
        return f"{self.model} ({self.team})"


class Racer(models.Model):
    RACER_CLASSES = [
        ('Pro', 'Профессионал'),
        ('Semi-pro', 'Полупрофессионал'),
        ('Amateur', 'Любитель'),
        ('Rookie', 'Новичок'),
    ]

    user = models.OneToOneField(RacingUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Команда")
    racer_class = models.CharField(max_length=20, choices=RACER_CLASSES, verbose_name="Класс гонщика")
    license_number = models.CharField(max_length=20, unique=True, verbose_name="Номер лицензии")
    wins_count = models.IntegerField(default=0, verbose_name="Количество побед")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Race(models.Model):
    RACE_TYPES = [
        ('Qualifying', 'Квалификация'),
        ('Sprint', 'Спринт'),
        ('Main', 'Основная гонка'),
        ('Championship', 'Чемпионат'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название гонки")
    race_type = models.CharField(max_length=20, choices=RACE_TYPES, verbose_name="Тип гонки")
    location = models.CharField(max_length=100, verbose_name="Место проведения")
    start_date = models.DateTimeField(verbose_name="Дата и время начала")
    end_date = models.DateTimeField(verbose_name="Дата и время окончания")
    description = models.TextField(blank=True, verbose_name="Описание гонки")
    is_active = models.BooleanField(default=True, verbose_name="Активная гонка")

    def __str__(self):
        return f"{self.name} ({self.location})"


class RaceRegistration(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE, verbose_name="Гонщик")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="Гонка")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждена")

    class Meta:
        unique_together = ['racer', 'race']

    def __str__(self):
        return f"{self.racer} - {self.race}"


class RaceResult(models.Model):
    race_registration = models.OneToOneField(RaceRegistration, on_delete=models.CASCADE, verbose_name="Регистрация")
    finish_time = models.DurationField(null=True, blank=True, verbose_name="Время финиша")
    position = models.IntegerField(null=True, blank=True, verbose_name="Позиция")
    best_lap_time = models.DurationField(null=True, blank=True, verbose_name="Лучшее время круга")
    points = models.IntegerField(default=0, verbose_name="Очки")
    dnf = models.BooleanField(default=False, verbose_name="Не финишировал")

    def __str__(self):
        return f"{self.race_registration.racer} - {self.position} место"


class Comment(models.Model):
    COMMENT_TYPES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('racing', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="Гонка")
    author = models.ForeignKey(RacingUser, on_delete=models.CASCADE, verbose_name="Автор")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария")
    text = models.TextField(verbose_name="Текст комментария")
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, verbose_name="Тип комментария")
    rating = models.IntegerField(
        verbose_name="Рейтинг (1-10)",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.author} - {self.race} ({self.comment_type})"
