from rest_framework import serializers
from .models import ReadingRoom, Reader, Book, BookCopy, Borrowing


# ============================================================
# СЕРИАЛИЗАТОРЫ — конвертируют объекты Django в JSON и обратно.
#
# Когда клиент (Vue) делает GET-запрос — сериализатор превращает
# объект Python в словарь → Django REST отдаёт его как JSON.
#
# Когда клиент делает POST/PUT — сериализатор принимает JSON,
# проверяет данные (валидация) и сохраняет в базу.
# ============================================================


class ReadingRoomSerializer(serializers.ModelSerializer):
    """
    Сериализатор читального зала.
    fields = '__all__' означает: включить все поля модели
    (id, number, name, capacity).
    """

    class Meta:
        model = ReadingRoom
        fields = '__all__'


class ReaderSerializer(serializers.ModelSerializer):
    """
    Сериализатор читателя.
    Добавляет поле reading_room_name — название зала строкой,
    чтобы фронтенд не делал отдельный запрос за именем зала.
    read_only=True означает: поле только для чтения, не принимается при POST.
    """

    # Дополнительное вычисляемое поле — берёт name у связанного зала
    reading_room_name = serializers.CharField(source='reading_room.name', read_only=True)

    class Meta:
        model = Reader
        fields = '__all__'   # включает и reading_room (id) и reading_room_name


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор книги.
    Возвращает все поля: id, title, authors, publisher,
    publication_year, section, cipher.
    """

    class Meta:
        model = Book
        fields = '__all__'


class BookCopySerializer(serializers.ModelSerializer):
    """
    Сериализатор экземпляра книги в зале.
    Добавляет читаемые названия book_title и room_name,
    чтобы фронтенд видел строки, а не только числовые id.
    """

    # Название книги — берётся из связанного объекта Book
    book_title = serializers.CharField(source='book.title', read_only=True)

    # Название зала — берётся из связанного объекта ReadingRoom
    room_name = serializers.CharField(source='reading_room.name', read_only=True)

    class Meta:
        model = BookCopy
        fields = '__all__'


class BorrowingSerializer(serializers.ModelSerializer):
    """
    Сериализатор выдачи книги.
    Добавляет book_title и reader_name для отображения в таблице
    (вместо числовых id книги и читателя).
    """

    # Название книги из связанной модели Book
    book_title = serializers.CharField(source='book.title', read_only=True)

    # Имя читателя из связанной модели Reader
    reader_name = serializers.CharField(source='reader.full_name', read_only=True)

    class Meta:
        model = Borrowing
        fields = '__all__'
