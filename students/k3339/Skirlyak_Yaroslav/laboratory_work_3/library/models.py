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
        max_length=50,
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
        through='BookAuthor',
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
        max_length=50,
        unique=True,
        verbose_name="Номер читательского билета"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="ФИО читателя"
    )
    passport_number = models.CharField(
        max_length=20,
        verbose_name="Номер паспорта"
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения"
    )
    address = models.TextField(
        verbose_name="Адрес проживания"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона"
    )
    education = models.CharField(
        max_length=100,
        verbose_name="Образование"
    )
    academic_degree = models.BooleanField(
        default=False,
        verbose_name="Наличие ученой степени"
    )
    registration_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Статус активности"
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
    copy_id = models.ForeignKey(
        'BookRoom',
        on_delete=models.CASCADE,
        verbose_name="Идентификатор экземпляра книги"
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name="Читатель"
    )
    date_assigned = models.DateField(
        verbose_name="Дата выдачи книги"
    )
    return_date = models.DateField(
        verbose_name="Ожидаемая дата сдачи"
    )
    actual_return_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Фактическая дата сдачи"
    )
    fine = models.FloatField(
        default=0.0,
        verbose_name="Штраф за просрочку"
    )
    fine_comment = models.TextField(
        null=True,
        blank=True,
        verbose_name="Комментарий к штрафу"
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
    copy_id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор экземпляра"
    )

    def __str__(self):
        return f"{self.book} в {self.room} (экземпляр: {self.copy_id})"


class BookAuthor(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Шифр книги"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Идентификатор автора"
    )

    def __str__(self):
        return f"{self.author} - {self.book}"


class ReaderRoomAssignment(models.Model):
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='room_assignments',
        verbose_name="Номер читательского билета"
    )
    room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.CASCADE,
        related_name='reader_assignments',
        verbose_name="Номер зала"
    )
    start_date = models.DateField(
        verbose_name="Дата начала закрепления"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания закрепления"
    )


    def __str__(self):
        return f"{self.reader} - {self.room}"
