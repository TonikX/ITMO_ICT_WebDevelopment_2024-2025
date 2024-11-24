from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name="Название категории")

    def __str__(self):
        return self.category_name


class Author(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="ФИО автора")

    def __str__(self):
        return self.full_name


class ReadingRoom(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name="Название")
    capacity = models.PositiveIntegerField(default=10,
                                           validators=[MinValueValidator(1), MaxValueValidator(30)],
                                           verbose_name="Вместимость")

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    publisher = models.CharField(max_length=50, verbose_name="Издательство")
    category = models.ManyToManyField(Category, related_name="category_books")
    authors = models.ManyToManyField(Author, related_name="author_books")

    def __str__(self):
        return self.name


class BookCopy(models.Model):
    book = models.ForeignKey(Book, related_name='copies', on_delete=CASCADE)
    cipher = models.CharField(max_length=10, verbose_name="Шифр книги")
    publishing_year = models.PositiveIntegerField(default=10,
                                                  validators=[MinValueValidator(868), MaxValueValidator(2023)],
                                                  verbose_name="Год публикации")

    def __str__(self):
        return f'{self.book.name} {self.cipher}'


class Reader(models.Model):
    reading_room = models.ForeignKey("ReadingRoom", related_name='who_in', on_delete=CASCADE, verbose_name="Закрепленный читальный зал")
    full_name = models.CharField(max_length=100, verbose_name="ФИО читателя")
    passport = models.CharField(max_length=20, verbose_name='Номер паспорта')
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    educations = (
        ('н', 'Начальное'),
        ('с', 'Среднее'),
        ('в', 'Высшее'),
    )
    education = models.CharField(max_length=1, choices=educations, verbose_name='Образование')
    degree = models.BooleanField(default=False, verbose_name='Наличие ученой степени')
    registration_date = models.DateField(verbose_name='Дата регистрации')
    reading_ticket = models.PositiveIntegerField(verbose_name="Номер читательского билета", default=0)

    def __str__(self):
        return self.full_name


class BookTake(models.Model):
    book_copy = models.ForeignKey(BookCopy, related_name='who_takes', on_delete=CASCADE, verbose_name="Взятая книга")
    reader = models.ForeignKey(Reader, related_name='what_is_taken', on_delete=CASCADE, verbose_name="Читатель")
    take_date = models.DateField(verbose_name="Дата, когда книга была взята")
    return_date = models.DateField(verbose_name="Дата, когда книга была возвращена")

    def __str__(self):
        return f'{self.book_copy.book.name} {self.reader.full_name}'