# Документация API библиотеки

Данный API предоставляет доступ к управлению библиотекой, включая модели книг, авторов, читателей и читальных залов. Реализация выполнена с использованием Django REST Framework и Djoser для аутентификации.

## Модель данных

### `models.py`

```python
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
```

## Важные блоки кода

### `serializers.py`

```python
from rest_framework import serializers
from .models import Book, Author, Reader, ReadingRoom, BookAssignment, BookRoom


class AuthorSerializer(serializers.ModelSerializer):
    num_books = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'num_books']


class ReadingRoomSerializer(serializers.ModelSerializer):
    num_readers = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReadingRoom
        fields = ['id', 'name', 'capacity', 'num_readers']


class BookRoomSerializer(serializers.ModelSerializer):
    room = ReadingRoomSerializer()

    class Meta:
        model = BookRoom
        fields = ['room', 'number_of_copies']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    rooms = BookRoomSerializer(source='bookroom_set', many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'book_code', 'title', 'publisher', 'year_of_publication',
            'section', 'authors', 'rooms'
        ]


class BookAssignmentSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    date_assigned = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = BookAssignment
        fields = ['book', 'date_assigned']


class ReaderSerializer(serializers.ModelSerializer):
    current_room = ReadingRoomSerializer(read_only=True)
    assigned_books = BookAssignmentSerializer(source='bookassignment_set', many=True, read_only=True)

    class Meta:
        model = Reader
        fields = [
            'id', 'reader_card_number', 'full_name', 'passport_number',
            'date_of_birth', 'address', 'phone_number', 'education',
            'academic_degree', 'current_room', 'registration_date',
            'is_active', 'assigned_books'
        ]
```

### `views.py`

```python
from django.db.models import Count, F
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Author, Reader, ReadingRoom, BookAssignment, BookRoom
from .serializers import (
    BookSerializer, AuthorSerializer, ReaderSerializer,
    ReadingRoomSerializer, BookAssignmentSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Фильтрация и поиск
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'publisher', 'section', 'authors__name']
    ordering_fields = ['year_of_publication', 'title']

    @action(detail=True, methods=['post'])
    def add_author(self, request, pk=None):
        book = self.get_object()
        author_id = request.data.get('author_id')
        try:
            author = Author.objects.get(id=author_id)
            book.authors.add(author)
            return Response({'status': 'Автор добавлен'})
        except Author.DoesNotExist:
            return Response({'status': 'Автор не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def assign_to_reader(self, request, pk=None):
        book = self.get_object()
        reader_id = request.data.get('reader_id')
        try:
            reader = Reader.objects.get(id=reader_id)
            BookAssignment.objects.create(book=book, reader=reader)
            return Response({'status': 'Книга закреплена за читателем'})
        except Reader.DoesNotExist:
            return Response({'status': 'Читатель не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def recent_books(self, request):
        recent_books = Book.objects.order_by('-year_of_publication')[:5]
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def books_by_section(self, request):
        section = request.query_params.get('section')
        if section:
            books = Book.objects.filter(section__icontains=section)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Параметр "section" обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def books_by_author(self, request):
        author_name = request.query_params.get('author_name')
        if author_name:
            books = Book.objects.filter(authors__name__icontains=author_name)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Параметр "author_name" обязателен'}, status=status.HTTP_400_BAD_REQUEST)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.annotate(num_books=Count('books'))
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def top_authors(self, request):
        top_authors = self.queryset.order_by('-num_books')[:5]
        serializer = self.get_serializer(top_authors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def assign_book(self, request, pk=None):
        reader = self.get_object()
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            BookAssignment.objects.create(book=book, reader=reader)
            return Response({'status': 'Книга закреплена за читателем'})
        except Book.DoesNotExist:
            return Response({'status': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def current_books(self, request, pk=None):
        reader = self.get_object()
        assignments = BookAssignment.objects.filter(reader=reader)
        books = [assignment.book for assignment in assignments]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active_readers(self, request):
        readers = Reader.objects.filter(is_active=True)
        serializer = self.get_serializer(readers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def readers_by_degree(self, request):
        degree = request.query_params.get('degree')
        if degree:
            readers = Reader.objects.filter(academic_degree__icontains=degree)
            serializer = self.get_serializer(readers, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Параметр "degree" обязателен'}, status=status.HTTP_400_BAD_REQUEST)


class ReadingRoomViewSet(viewsets.ModelViewSet):
    queryset = ReadingRoom.objects.annotate(num_readers=Count('readers'))
    serializer_class = ReadingRoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        room = self.get_object()
        book_rooms = BookRoom.objects.filter(room=room)
        books = [br.book for br in book_rooms]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_rooms(self, request):
        available_rooms = ReadingRoom.objects.annotate(
            num_readers=Count('readers')
        ).filter(num_readers__lt=F('capacity'))
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def rooms_by_capacity(self, request):
        min_capacity = request.query_params.get('min_capacity', 0)
        max_capacity = request.query_params.get('max_capacity', 100)
        rooms = ReadingRoom.objects.filter(
            capacity__gte=min_capacity,
            capacity__lte=max_capacity
        )
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
```

## API эндпоинты

### Аутентификация

Все запросы требуют аутентификации по токену. Токен передается в заголовке `Authorization`.

**Пример заголовка:**

```
Authorization: Token your_auth_token
```

### Авторы (`/api/authors/`)

- **GET** `/api/authors/` — Получить список всех авторов.
- **POST** `/api/authors/` — Создать нового автора.

#### Детальные действия с автором (`/api/authors/{id}/`)

- **GET** `/api/authors/{id}/` — Получить информацию об авторе.
- **PUT** `/api/authors/{id}/` — Полностью обновить информацию об авторе.
- **PATCH** `/api/authors/{id}/` — Частично обновить информацию об авторе.
- **DELETE** `/api/authors/{id}/` — Удалить автора.

#### Пользовательские действия с автором

- **GET** `/api/authors/top_authors/` — Получить топ-5 авторов по количеству книг.
- **GET** `/api/authors/{id}/books/` — Получить список книг автора.

### Книги (`/api/books/`)

- **GET** `/api/books/` — Получить список всех книг.
- **POST** `/api/books/` — Создать новую книгу.

#### Детальные действия с книгой (`/api/books/{id}/`)

- **GET** `/api/books/{id}/` — Получить информацию о книге.
- **PUT** `/api/books/{id}/` — Полностью обновить информацию о книге.
- **PATCH** `/api/books/{id}/` — Частично обновить информацию о книге.
- **DELETE** `/api/books/{id}/` — Удалить книгу.

#### Пользовательские действия с книгой

- **POST** `/api/books/{id}/add_author/` — Добавить автора к книге.
  - **Параметры:**
    - `author_id` (int) — ID автора.
- **POST** `/api/books/{id}/assign_to_reader/` — Закрепить книгу за читателем.
  - **Параметры:**
    - `reader_id` (int) — ID читателя.
- **GET** `/api/books/recent_books/` — Получить 5 самых новых книг.
- **GET** `/api/books/books_by_section/?section=...` — Получить книги по разделу.
- **GET** `/api/books/books_by_author/?author_name=...` — Получить книги по имени автора.

### Читатели (`/api/readers/`)

- **GET** `/api/readers/` — Получить список всех читателей.
- **POST** `/api/readers/` — Создать нового читателя.

#### Детальные действия с читателем (`/api/readers/{id}/`)

- **GET** `/api/readers/{id}/` — Получить информацию о читателе.
- **PUT** `/api/readers/{id}/` — Полностью обновить информацию о читателе.
- **PATCH** `/api/readers/{id}/` — Частично обновить информацию о читателе.
- **DELETE** `/api/readers/{id}/` — Удалить читателя.

#### Пользовательские действия с читателем

- **POST** `/api/readers/{id}/assign_book/` — Закрепить книгу за читателем.
  - **Параметры:**
    - `book_id` (int) — ID книги.
- **GET** `/api/readers/{id}/current_books/` — Получить список текущих книг читателя.
- **GET** `/api/readers/active_readers/` — Получить список активных читателей.
- **GET** `/api/readers/readers_by_degree/?degree=...` — Получить читателей по ученой степени.

### Читальные залы (`/api/reading-rooms/`)

- **GET** `/api/reading-rooms/` — Получить список всех читальных залов.
- **POST** `/api/reading-rooms/` — Создать новый читальный зал.

#### Детальные действия с читальным залом (`/api/reading-rooms/{id}/`)

- **GET** `/api/reading-rooms/{id}/` — Получить информацию о читальном зале.
- **PUT** `/api/reading-rooms/{id}/` — Полностью обновить информацию о зале.
- **PATCH** `/api/reading-rooms/{id}/` — Частично обновить информацию о зале.
- **DELETE** `/api/reading-rooms/{id}/` — Удалить зал.

#### Пользовательские действия с читальным залом

- **GET** `/api/reading-rooms/{id}/books/` — Получить список книг в зале.
- **GET** `/api/reading-rooms/available_rooms/` — Получить залы с доступными местами.
- **GET** `/api/reading-rooms/rooms_by_capacity/?min_capacity=...&max_capacity=...` — Фильтровать залы по вместимости.

## Примеры использования эндпоинтов

### Получение списка книг

```
GET /api/books/
```

**Параметры запроса:**

- `search` — Поиск по названию, издательству, разделу или имени автора.
- `ordering` — Сортировка по `year_of_publication` или `title`.

**Пример:**

```
GET /api/books/?search=Python&ordering=-year_of_publication
```

### Закрепление книги за читателем

```
POST /api/books/{id}/assign_to_reader/
```

**Тело запроса:**

```json
{
  "reader_id": 1
}
```

### Поиск читателей по ученой степени

```
GET /api/readers/readers_by_degree/?degree=Доктор наук
```

## Аутентификация и регистрация

### Регистрация пользователя

```
POST /auth/users/
```

**Тело запроса:**

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

### Получение токена

```
POST /auth/token/login/
```

**Тело запроса:**

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

**Ответ:**

```json
{
  "auth_token": "your_auth_token"
}
```