from django.db import models
from django.contrib.auth.models import AbstractUser


# Пользователи
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('editor', 'Редактор'),
        ('user', 'Пользователь'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    patronymic = models.CharField("Отчество", max_length=150, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'patronymic', 'role']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''} ({self.role})"


# Газеты
class Newspaper(models.Model):
    name = models.CharField("Название газеты", max_length=255)
    index = models.CharField("Индекс", max_length=20, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    editor = models.ForeignKey(
        User,
        verbose_name="Редактор",
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'editor'},
        related_name='newspapers'
    )

    def __str__(self):
        return f"Газета: {self.name} (Индекс: {self.index})"


# Типографии
class PrintingHouse(models.Model):
    name = models.CharField("Название типографии", max_length=255)
    address = models.TextField("Адрес")
    is_active = models.BooleanField("Типография открыта?", default=True)

    def __str__(self):
        status = "Открыта" if self.is_active else "Закрыта"
        return f"Типография: {self.name} ({status})"


# Почтовые отделения
class PostOffice(models.Model):
    number = models.IntegerField("Номер отделения")
    address = models.TextField("Адрес")

    def __str__(self):
        return f"Почтовое отделение №{self.number} ({self.address})"


# Тиражи
class Edition(models.Model):
    printing_house = models.ForeignKey(
        PrintingHouse,
        verbose_name="Типография",
        on_delete=models.CASCADE,
        related_name='editions'
    )
    newspaper = models.ForeignKey(
        Newspaper,
        verbose_name="Газета",
        on_delete=models.CASCADE,
        related_name='editions'
    )
    quantity = models.PositiveIntegerField("Тираж")

    def __str__(self):
        return f"Тираж газеты {self.newspaper.name} ({self.quantity} экземпляров)"


# Поставки
class Distribution(models.Model):
    post_office = models.ForeignKey(
        PostOffice,
        verbose_name="Почтовое отделение",
        on_delete=models.CASCADE,
        related_name='distributions'
    )
    printing_house = models.ForeignKey(
        PrintingHouse,
        verbose_name="Типография",
        on_delete=models.CASCADE,
        related_name='distributions'
    )
    newspaper = models.ForeignKey(
        Newspaper,
        verbose_name="Газета",
        on_delete=models.CASCADE,
        related_name='distributions'
    )
    quantity = models.PositiveIntegerField("Количество")

    def __str__(self):
        return f"Поставка: {self.newspaper.name} ({self.quantity} экз.) → Почтовое отделение №{self.post_office.number}"