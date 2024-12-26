from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя автора"
    )

    def __str__(self):
        return self.name


class ReadingRoom(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название зала"
    )
    capacity = models.PositiveIntegerField(
        verbose_name="Вместимость"
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    book_code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Шифр книги"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название книги"
    )
    publisher = models.CharField(
        max_length=255,
        verbose_name="Издательство"
    )
    year_of_publication = models.PositiveIntegerField(
        verbose_name="Год издания"
    )
    section = models.CharField(
        max_length=255,
        verbose_name="Раздел"
    )
    authors = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name="Авторы"
    )
    rooms = models.ManyToManyField(
        ReadingRoom,
        through='BookRoom',
        related_name='books',
        verbose_name="Залы"
    )

    def __str__(self):
        return self.title


class Reader(models.Model):
    reader_card_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Номер читательского билета"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="ФИО читателя"
    )
    passport_number = models.CharField(
        max_length=50,
        verbose_name="Номер паспорта"
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения"
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона"
    )
    education = models.CharField(
        max_length=255,
        verbose_name="Образование"
    )
    academic_degree = models.CharField(
        max_length=255,
        verbose_name="Наличие ученой степени"
    )
    current_room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.SET_NULL,
        null=True,
        related_name='readers',
        verbose_name="Текущий номер зала"
    )
    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    assigned_books = models.ManyToManyField(
        Book,
        through='BookAssignment',
        related_name='assigned_readers',
        verbose_name="Закрепленные книги"
    )

    def __str__(self):
        return self.full_name


class BookAssignment(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга"
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name="Читатель"
    )
    date_assigned = models.DateField(
        auto_now_add=True,
        verbose_name="Дата закрепления за читателем"
    )

    def __str__(self):
        return f"{self.book} закреплена за {self.reader}"


class BookRoom(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга"
    )
    room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.CASCADE,
        verbose_name="Читальный зал"
    )
    number_of_copies = models.PositiveIntegerField(
        verbose_name="Число экземпляров"
    )

    def __str__(self):
        return f"{self.book} в {self.room} (экземпляров: {self.number_of_copies})"
