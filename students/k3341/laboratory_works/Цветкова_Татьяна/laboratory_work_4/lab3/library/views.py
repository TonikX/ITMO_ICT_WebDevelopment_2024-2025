from django.contrib.auth.models import User
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import ReadingRoom, Reader, Book, BookCopy, Borrowing
from .serializers import (
    ReadingRoomSerializer,
    ReaderSerializer,
    BookSerializer,
    BookCopySerializer,
    BorrowingSerializer,
)


# ============================================================
# VIEWS (представления) — обрабатывают HTTP-запросы от клиента.
#
# ModelViewSet автоматически создаёт 5 методов:
#   list()    — GET /api/rooms/         → список всех объектов
#   retrieve()— GET /api/rooms/{id}/    → один объект
#   create()  — POST /api/rooms/        → создать новый
#   update()  — PUT /api/rooms/{id}/    → полностью обновить
#   destroy() — DELETE /api/rooms/{id}/ → удалить
# ============================================================


class ReadingRoomViewSet(viewsets.ModelViewSet):
    """
    CRUD для читальных залов.
    Фронтенд использует этот ViewSet на странице /rooms.
    """

    # Все залы из базы
    queryset = ReadingRoom.objects.all()

    # Используем ReadingRoomSerializer для преобразования в JSON
    serializer_class = ReadingRoomSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    """
    CRUD для читателей.
    select_related('reading_room') — оптимизация: загружает данные
    зала за один SQL-запрос вместо N дополнительных запросов.
    """

    queryset = Reader.objects.select_related('reading_room').all()
    serializer_class = ReaderSerializer

    # Подключаем фильтрацию и поиск
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # По каким полям можно фильтровать: /api/readers/?is_active=true
    filterset_fields = ['is_active', 'reading_room', 'education']

    # По каким полям работает поиск: /api/readers/?search=Иванов
    search_fields = ['full_name', 'ticket_number']


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD для книг.
    Фронтенд использует на странице /books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Фильтрация по разделу, издательству, году: /api/books/?section=Классика
    filterset_fields = ['section', 'publisher', 'publication_year']

    # Поиск по названию и автору: /api/books/?search=Толстой
    search_fields = ['title', 'authors']


class BookCopyViewSet(viewsets.ModelViewSet):
    """
    CRUD для экземпляров книг по залам.
    Через этот ViewSet библиотекарь управляет количеством
    физических копий каждой книги в каждом зале.
    """

    queryset = BookCopy.objects.select_related('book', 'reading_room').all()
    serializer_class = BookCopySerializer

    filter_backends = [DjangoFilterBackend]

    # Фильтрация: /api/bookcopies/?book=1 или ?reading_room=2
    filterset_fields = ['book', 'reading_room']


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    CRUD для выдачи книг читателям.
    Переопределяем create() и update() для управления
    количеством экземпляров при выдаче и возврате.
    """

    queryset = Borrowing.objects.select_related('book', 'reader').all()
    serializer_class = BorrowingSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reader', 'book']

    def create(self, request, *args, **kwargs):
        """
        POST /api/borrowings/ — выдать книгу читателю.

        Логика:
        1. Ищем экземпляр книги (BookCopy) в любом зале.
        2. Если экземпляров нет или их 0 → возвращаем ошибку 400.
        3. Если есть → уменьшаем количество на 1 и создаём запись Borrowing.
        """

        book_id = request.data.get('book')

        # Ищем первый попавшийся экземпляр этой книги в любом зале
        copy = BookCopy.objects.filter(book_id=book_id).first()

        # Проверка: есть ли физический экземпляр для выдачи
        if not copy or copy.quantity <= 0:
            return Response(
                {'error': 'Книга отсутствует в читальном зале'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Уменьшаем счётчик доступных экземпляров на 1
        copy.quantity -= 1
        copy.save()

        # Вызываем стандартный метод создания записи Borrowing
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        PATCH /api/borrowings/{id}/ — обновить запись (в том числе вернуть книгу).

        Логика возврата:
        Если в запросе пришло return_date и раньше оно было пустым
        (книга ещё не возвращалась) → увеличиваем счётчик экземпляров на 1.
        """

        instance = self.get_object()  # текущая запись о выдаче

        # Проверяем: пришла ли дата возврата и не была ли она уже установлена
        if request.data.get('return_date') and not instance.return_date:
            copy = BookCopy.objects.filter(book=instance.book).first()
            if copy:
                # Книга возвращена — увеличиваем количество доступных экземпляров
                copy.quantity += 1
                copy.save()

        # Вызываем стандартный метод обновления
        return super().update(request, *args, **kwargs)


# ============================================================
# Отдельный view для регистрации пользователя-библиотекаря.
# Использует Djoser через /auth/users/, но здесь оставлен
# собственный эндпоинт /api/register/ как запасной вариант.
# ============================================================

@api_view(['POST'])
@permission_classes([AllowAny])   # доступен без авторизации (нужно для регистрации)
def register(request):
    """
    POST /api/register/ — создать нового пользователя.
    Принимает: { "username": "...", "password": "..." }
    """

    username = request.data.get('username')
    password = request.data.get('password')

    # Проверка: переданы ли оба поля
    if not username or not password:
        return Response({'error': 'Введите логин и пароль'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка: не существует ли уже такой пользователь
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    # Создаём пользователя — create_user автоматически хэширует пароль
    User.objects.create_user(username=username, password=password)
    return Response({'message': 'Пользователь создан'}, status=status.HTTP_201_CREATED)
