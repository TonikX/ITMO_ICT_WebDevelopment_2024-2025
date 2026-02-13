from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название команды')
    description = models.TextField(blank=True, null=True, verbose_name='Описание команды')
    founded_year = models.IntegerField(blank=True, null=True, verbose_name='Год основания')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class Driver(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Новичок'),
        ('intermediate', 'Промежуточный'),
        ('advanced', 'Продвинутый'),
        ('professional', 'Профессионал'),
    ]

    CLASS_CHOICES = [
        ('a', 'Класс A'),
        ('b', 'Класс B'),
        ('c', 'Класс C'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Команда')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name='Опыт')
    driver_class = models.CharField(max_length=10, choices=CLASS_CHOICES, verbose_name='Класс')
    description = models.TextField(blank=True, null=True, verbose_name='Описание водителя')

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Car(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True, verbose_name='Описание автомобиля')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Race(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название гонки')
    date = models.DateTimeField(verbose_name='Дата и время')
    location = models.CharField(max_length=100, verbose_name='Место проведения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание гонки')

    class Meta:
        verbose_name = 'Гонка'
        verbose_name_plural = 'Гонки'
        ordering = ['-date']

    def __str__(self):
        return self.name


class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results', verbose_name='Гонка')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    position = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Место')
    time = models.CharField(max_length=20, blank=True, null=True, verbose_name='Время')
    points = models.IntegerField(default=0, verbose_name='Очки')

    class Meta:
        verbose_name = 'Результат гонки'
        verbose_name_plural = 'Результаты гонок'
        unique_together = ('race', 'driver')

    def __str__(self):
        return f"{self.driver} - {self.race} ({self.position})"


class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('collaboration', 'Вопрос о сотрудничестве'),
        ('racing', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments', verbose_name='Гонка')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    race_date = models.DateField(auto_now_add=True, verbose_name='Дата комментария')
    text = models.TextField(verbose_name='Текст комментария')
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES, verbose_name='Тип комментария')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} - {self.race}"


class Registration(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='registrations', verbose_name='Водитель')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registrations', verbose_name='Гонка')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')

    class Meta:
        verbose_name = 'Регистрация на гонку'
        verbose_name_plural = 'Регистрации на гонку'
        unique_together = ('driver', 'race')

    def __str__(self):
        return f"{self.driver} - {self.race}"
