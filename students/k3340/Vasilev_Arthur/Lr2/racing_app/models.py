from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    EXPERIENCE_LEVEL = [
        ('NB', 'Новичок'),
        ('SP', 'Любитель'),
        ('PR', 'Профессионал'),
    ]
    
    experience = models.CharField(
        'Уровень опыта',
        max_length=2, 
        choices=EXPERIENCE_LEVEL, 
        default='NB'
    )
    driver_class = models.CharField(
        'Класс гонщика', 
        max_length=50, 
        blank=True, 
        null=True
    )
    bio = models.TextField(
        'Биография', 
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_experience_display()})"

class Team(models.Model):
    name = models.CharField(
        'Название команды',
        max_length=100, 
        unique=True
    )
    description = models.TextField(
        'Описание команды',
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.name

class Car(models.Model):
    owner = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='car',
        verbose_name='Владелец'
    )
    team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='cars',
        verbose_name='Команда'
    )
    model = models.CharField(
        'Модель автомобиля',
        max_length=100
    )
    description = models.TextField(
        'Описание автомобиля'
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.model} - {self.owner.username}"

class Race(models.Model):
    name = models.CharField(
        'Название гонки',
        max_length=200
    )
    description = models.TextField(
        'Описание гонки',
        blank=True, 
        null=True
    )
    date = models.DateTimeField(
        'Дата и время заезда'
    )
    location = models.CharField(
        'Место проведения',
        max_length=200,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        'Активная гонка',
        default=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.date.date()})"

class RaceRegistration(models.Model):
    racer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='registrations',
        verbose_name='Гонщик'
    )
    race = models.ForeignKey(
        Race, 
        on_delete=models.CASCADE, 
        related_name='registrations',
        verbose_name='Гонка'
    )
    registration_date = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    result = models.CharField(
        'Результат',
        max_length=100, 
        blank=True, 
        null=True
    )
    final_time = models.DurationField(
        'Финальное время',
        blank=True, 
        null=True
    )
    position = models.PositiveIntegerField(
        'Позиция',
        blank=True, 
        null=True
    )

    class Meta:
        unique_together = ['racer', 'race']
        ordering = ['position', 'final_time']

    def __str__(self):
        return f"{self.racer} -> {self.race}"

class Comment(models.Model):
    COMMENT_TYPES = [
        ('COOP', 'Вопрос о сотрудничестве'),
        ('RACE', 'Вопрос о гонках'),
        ('OTHER', 'Иное'),
    ]
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Автор'
    )
    race = models.ForeignKey(
        Race, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Гонка'
    )
    text = models.TextField('Текст комментария')
    type = models.CharField(
        'Тип комментария',
        max_length=5, 
        choices=COMMENT_TYPES, 
        default='RACE'
    )
    rating = models.IntegerField(
        'Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    is_approved = models.BooleanField(
        'Одобрен',
        default=True
    )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"Комментарий от {self.author} к {self.race}"