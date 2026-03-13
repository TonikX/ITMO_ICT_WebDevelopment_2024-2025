from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ReadingRoomViewSet,
    ReaderViewSet,
    BookViewSet,
    BookCopyViewSet,
    BorrowingViewSet,
    register,
)


# ============================================================
# URL-маршруты приложения library
#
# DefaultRouter автоматически генерирует все нужные URL
# для каждого ViewSet (list, detail, create, update, delete).
#
# Пример сгенерированных маршрутов для 'books':
#   GET    /api/books/        → список книг
#   POST   /api/books/        → добавить книгу
#   GET    /api/books/{id}/   → одна книга
#   PUT    /api/books/{id}/   → обновить книгу
#   PATCH  /api/books/{id}/   → частично обновить
#   DELETE /api/books/{id}/   → удалить книгу
# ============================================================

# Создаём роутер
router = DefaultRouter()

# Регистрируем ViewSet-ы: prefix — часть URL, ViewSet — класс обработчика
router.register('rooms', ReadingRoomViewSet)         # /api/rooms/
router.register('readers', ReaderViewSet)             # /api/readers/
router.register('books', BookViewSet)                 # /api/books/
router.register('bookcopies', BookCopyViewSet)        # /api/bookcopies/
router.register('borrowings', BorrowingViewSet)       # /api/borrowings/

urlpatterns = [
    # Отдельный маршрут для регистрации пользователя
    path('register/', register),   # /api/register/

    # Все маршруты, сгенерированные роутером
] + router.urls
