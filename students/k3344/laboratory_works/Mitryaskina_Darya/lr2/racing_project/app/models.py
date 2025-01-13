from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Email должен быть указан')
        if not full_name:
            raise ValueError('Полное имя должно быть указано')

        email = self.normalize_email(email)

        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email, full_name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Email')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Race(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    date = models.DateTimeField(verbose_name='Дата')
    location = models.CharField(max_length=100, verbose_name='Место')
    result = models.CharField(max_length=100, blank=True, null=True, verbose_name='Результат')

    def __str__(self):
        return f'{self.name} - {self.date.strftime("%Y-%m-%d %H:%M")}'


class Registration(models.Model):

    CLASS_LEVEL = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='registration')
    team_name = models.CharField(max_length=100, verbose_name='Название команды')
    car_description = models.TextField(verbose_name='Описание гоночной машины')
    racer_description = models.TextField(verbose_name='Описание гонщика')
    experience = models.IntegerField(verbose_name='Опыт в годах')
    class_level = models.CharField(max_length=10, choices=CLASS_LEVEL, verbose_name='Уровень')

    def __str__(self):
        return f'{self.user.email} - {self.race.name}'
    

class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('collaboration', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')
    comment_type = models.CharField(max_length=50, choices=COMMENT_TYPE_CHOICES, verbose_name='Назначение')
    rating = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 11)], verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.full_name} к {self.race.name}'

    def get_race_date(self):
        return self.race.date.strftime("%Y-%m-%d %H:%M")
    

