from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class Genre(models.Model):
    """
    Модель жанра
    """

    title = models.CharField(max_length=50,
                             verbose_name="Название жанра")

class Author(models.Model):
    """
    Модель автора
    """

    full_name = models.CharField(max_length=120,
                                 verbose_name="ФИО автора")

class Book(models.Model):
    """
    Модель оригинала книги
    """

    title = models.CharField(max_length=150, 
                             verbose_name="Книга")
    
    publisher = models.CharField(max_length=50,
                                 verbose_name="Издательство")
    
    genre = models.ManyToManyField("Genre",
                                   through="BookGenre",
                                   verbose_name="Жанры",
                                   related_name="book_genre")
    
    author = models.ManyToManyField("Author",
                                    through="BookAuthor",
                                    verbose_name="Авторы",
                                    related_name="book_author")
    
class BookGenre(models.Model):
    """
    Модель жанра конкретной книги 
    """

    book = models.ForeignKey("Book",
                             verbose_name="Книга",
                             on_delete=models.CASCADE)
    
    genre = models.ForeignKey("Genre",
                              verbose_name="Жанр",
                              on_delete=models.CASCADE)

class BookAuthor(models.Model):
    """
    Модель автора книги
    """

    book = models.ForeignKey("Book",
                             verbose_name="Книга",
                             on_delete=models.CASCADE)
    
    author = models.ForeignKey("Author",
                               verbose_name="Автор",
                               on_delete=models.CASCADE)

class BookCopy(models.Model):
    """
    Модель копии книги
    """

    def current_year():
        return now().year

    book = models.ForeignKey("Book",
                             verbose_name="Книга",
                             on_delete=models.CASCADE)
    
    cipher = models.CharField(max_length=10,
                              verbose_name="Шифр книги")
    
    publish_year = models.PositiveIntegerField(default=current_year, 
                                               verbose_name="Год публикации",
                                               validators=[MinValueValidator(1000), 
                                               MaxValueValidator(2097)])

class ReadingRoom(models.Model):
    """
    Модель читального зала
    """

    name = models.CharField(max_length=30,
                            verbose_name="Название зала")

    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    
class Reader(models.Model):
    """
    Модель читателя
    """

    def today():
        return now().date()

    full_name = models.CharField(max_length=120,
                                 verbose_name="ФИО читателя")
    
    passport_number = models.CharField(max_length=16,
                                       verbose_name="Номер паспорта")
    
    birthdate = models.DateField(verbose_name="Дата рождения")

    address = models.CharField(max_length=100,
                               verbose_name="Адрес")
    
    phone_number = models.CharField(max_length=20,
                                    verbose_name="Номер телефона")
    
    education_types = (
        ("н", "начальное"),
        ("с", "среднее"),
        ("в", "высшее")
    )

    education = models.CharField(default="н",
                                 max_length=1,
                                 choices=education_types,
                                 verbose_name="Образование")
    
    degree = models.BooleanField(default=False,
                                 verbose_name="Наличие учёной степени")
    
    registration_date = models.DateField(default=today, 
                                         verbose_name="Дата регистрации")
    
    reading_ticket_number = models.CharField(max_length=10,
                                             verbose_name="Номер читательного билета")
    
    reading_room = models.ForeignKey("ReadingRoom",
                                     verbose_name="Читальный зал",
                                     related_name="reader_room",
                                     on_delete=models.CASCADE)
    
class BookTake(models.Model):
    """
    Модель взятия книги
    """

    def today():
        return now().date()

    book_copy = models.ForeignKey("BookCopy",
                             verbose_name="Взятая копия книги",
                             related_name="book_taken",
                             on_delete=models.CASCADE)
    
    reader = models.ForeignKey("Reader",
                               verbose_name="Читатель",
                               related_name="who_took",
                               on_delete=models.CASCADE)
    
    take_date = models.DateField(default=today,
                                 verbose_name="Дата взятия")
    
    restore_date = models.DateField(blank=True, null=True,
                                    verbose_name="Дата возврата")
