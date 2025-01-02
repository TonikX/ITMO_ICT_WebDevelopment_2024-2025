from django.db.models import Count, F
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book, Author, Reader, ReadingRoom, BookAssignment, BookRoom
from .serializers import (
    BookSerializer, AuthorSerializer, ReaderSerializer,
    ReadingRoomSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

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
    queryset = ReadingRoom.objects.annotate(num_readers=Count('reader_assignments'))
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