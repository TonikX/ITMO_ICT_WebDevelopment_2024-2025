from django.db import models


class ReadingRoom(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Reader(models.Model):
    ticket_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=20)

    EDUCATION_CHOICES = [
        ('primary', 'Начальное'),
        ('secondary', 'Среднее'),
        ('higher', 'Высшее'),
    ]

    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    has_degree = models.BooleanField(default=False)

    reading_room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.SET_NULL,
        null=True,
        related_name='readers'
    )

    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    section = models.CharField(max_length=100)
    cipher = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.reader} - {self.book}"