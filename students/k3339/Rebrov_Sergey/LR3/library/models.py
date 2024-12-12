from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username


class Publisher(models.Model):
    name = models.CharField(max_length=128, null=False)
    year = models.IntegerField(null=False)

    def __str__(self):
        return f"({self.name} {self.year})"


class Author(models.Model):
    surname = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=128, null=False)
    patronymic = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"({self.name} {self.surname})"


class Book(models.Model):
    name = models.CharField(max_length=128, null=False)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    cipher = models.CharField(max_length=128, null=False)

    def __str__(self):
        return f"({self.name})"


class Library(models.Model):
    name = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"({self.name}"


class Hall(models.Model):
    number = models.IntegerField(null=False)
    name = models.CharField(max_length=128, null=True)
    capacity = models.IntegerField(null=False)
    library = models.ForeignKey(Library, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.number} {self.library})"


class Reader(models.Model):
    surname = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=128, null=False)
    patronymic = models.CharField(max_length=128, null=True)
    ticket = models.CharField(max_length=128, null=False)
    passport = models.CharField(max_length=128, null=False)
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=128, null=False)
    education = models.CharField(max_length=128, null=True)
    is_academic = models.BooleanField(default=False, null=False)
    hall = models.ForeignKey(Hall, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"({self.name} {self.surname})"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.book} {self.author})"


class BookReader(models.Model):
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, null=False, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"({self.book} {self.reader})"


class BookHall(models.Model):
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, null=False, on_delete=models.CASCADE)
    count = models.IntegerField(null=False)

    def __str__(self):
        return f"({self.book} {self.hall})"
