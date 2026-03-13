from django.db import models


# ============================================================
# МОДЕЛИ БАЗЫ ДАННЫХ — описывают таблицы в SQLite через Django ORM
# Каждый класс = одна таблица. Поля класса = столбцы таблицы.
# ============================================================


class ReadingRoom(models.Model):
    """
    Читальный зал библиотеки.
    Книги и читатели привязываются к конкретному залу.
    """

    # Уникальный номер зала (например, 1, 2, 3)
    number = models.IntegerField(unique=True)

    # Название зала (например, "Большой читальный зал")
    name = models.CharField(max_length=100)

    # Вместимость — сколько людей могут одновременно работать в зале
    capacity = models.IntegerField()

    class Meta:
        verbose_name = 'Читальный зал'
        verbose_name_plural = 'Читальные залы'

    def __str__(self):
        # Строковое представление объекта — видно в Django Admin
        return f"Зал №{self.number} — {self.name}"


class Reader(models.Model):
    """
    Читатель библиотеки.
    Хранит личные данные и привязку к читальному залу.
    """

    # Варианты уровня образования для поля education
    EDUCATION_CHOICES = [
        ('primary', 'Начальное'),
        ('secondary', 'Среднее'),
        ('higher', 'Высшее'),
    ]

    # Номер читательского билета — уникальный идентификатор читателя
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name='Номер билета')

    # Полное имя читателя
    full_name = models.CharField(max_length=255, verbose_name='ФИО')

    # Номер паспорта
    passport_number = models.CharField(max_length=20, verbose_name='Паспорт')

    # Дата рождения
    birth_date = models.DateField(verbose_name='Дата рождения')

    # Адрес проживания
    address = models.TextField(verbose_name='Адрес')

    # Телефон
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    # Уровень образования — выбор из EDUCATION_CHOICES
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name='Образование')

    # Наличие учёной степени (True/False)
    has_degree = models.BooleanField(default=False, verbose_name='Учёная степень')

    # Внешний ключ на ReadingRoom — читатель закреплён за залом
    # SET_NULL — если зал удалят, поле станет NULL (читатель не удалится)
    reading_room = models.ForeignKey(
        ReadingRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='readers',   # обратная связь: room.readers.all()
        verbose_name='Читальный зал',
    )

    # Дата регистрации — ставится автоматически при создании
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    # Активен ли читатель (True = записан, False = выписан)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self):
        return f"{self.full_name} (билет {self.ticket_number})"


class Book(models.Model):
    """
    Книга в библиотеке.
    Хранит библиографические данные. Количество экземпляров
    по залам хранится в модели BookCopy.
    """

    # Название книги
    title = models.CharField(max_length=255, verbose_name='Название')

    # Авторы — строкой через запятую (например, "Л. Толстой, М. Горький")
    authors = models.CharField(max_length=255, verbose_name='Авторы')

    # Издательство
    publisher = models.CharField(max_length=255, verbose_name='Издательство')

    # Год издания (целое число, например 1869)
    publication_year = models.IntegerField(verbose_name='Год издания')

    # Раздел (тематика, например "Классика", "Наука")
    section = models.CharField(max_length=100, verbose_name='Раздел')

    # Шифр книги — уникальный код для поиска на полке
    cipher = models.CharField(max_length=50, verbose_name='Шифр')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.title} / {self.authors}"


class BookCopy(models.Model):
    """
    Экземпляры книги в конкретном читальном зале.
    Связывает книгу с залом и хранит количество доступных копий.

    Пример: "Война и мир" — 3 экземпляра в Зале №1, 2 — в Зале №2.
    """

    # Ссылка на книгу (при удалении книги удаляются и все её копии — CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies', verbose_name='Книга')

    # Ссылка на зал, где находятся экземпляры
    reading_room = models.ForeignKey(ReadingRoom, on_delete=models.CASCADE, related_name='book_copies', verbose_name='Зал')

    # Количество физических экземпляров этой книги в данном зале
    quantity = models.IntegerField(default=0, verbose_name='Количество экземпляров')

    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        # Одна книга не может быть дважды в одном зале — комбинация уникальна
        unique_together = ('book', 'reading_room')

    def __str__(self):
        return f"{self.book} — {self.reading_room} ({self.quantity} экз.)"


class Borrowing(models.Model):
    """
    Факт выдачи книги читателю.
    Когда читатель берёт книгу — создаётся запись.
    Когда возвращает — заполняется поле return_date.
    """

    # Какая книга выдана
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings', verbose_name='Книга')

    # Кому выдана
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='borrowings', verbose_name='Читатель')

    # Дата выдачи — проставляется автоматически при создании записи
    borrow_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')

    # Дата возврата — NULL пока книга на руках, заполняется при возврате
    return_date = models.DateField(null=True, blank=True, verbose_name='Дата возврата')

    class Meta:
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдача книг'

    def __str__(self):
        return f"{self.reader} → {self.book}"
