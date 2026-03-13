from rest_framework import viewsets

from .models import ReadingRoom, Reader, Book, Borrowing
from .serializers import (
    ReadingRoomSerializer,
    ReaderSerializer,
    BookSerializer,
    BorrowingSerializer
)


class ReadingRoomViewSet(viewsets.ModelViewSet):
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer