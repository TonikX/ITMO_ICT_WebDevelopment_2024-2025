from datetime import date
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializer import *


class BooksAPIView(ListCreateAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BookReadSerializer
        return BookWriteSerializer


class BookAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BookReadSerializer
        return BookWriteSerializer


class AuthorsAPIView(ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class AuthorAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class PublishersAPIView(ListCreateAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()


class PublisherAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()


class LibrariesAPIView(ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()


class LibraryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()


class HallsAPIView(ListCreateAPIView):
    queryset = Hall.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return HallReadSerializer
        return HallWriteSerializer


class HallAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Hall.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return HallReadSerializer
        return HallWriteSerializer


class ReadersAPIView(ListCreateAPIView):
    queryset = Reader.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ReaderReadSerializer
        return ReaderWriteSerializer


class ReaderAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Reader.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ReaderReadSerializer
        return ReaderWriteSerializer


class RentBookAPIView(APIView):
    def post(self, request):
        serializer = BookReaderRequestSerializer(data=request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book']
            reader_id = serializer.validated_data['reader']

            try:
                book = Book.objects.get(id=book_id)
                reader = Reader.objects.get(id=reader_id)
            except (Book.DoesNotExist, Reader.DoesNotExist):
                return Response({"detail": "Book or Reader not found"}, status=status.HTTP_404_NOT_FOUND)

            hall = reader.hall

            book_hall = BookHall.objects.filter(book=book, hall=hall).first()

            if not book_hall or book_hall.count <= 0:
                return Response({"detail": "Book not available in this hall"}, status=status.HTTP_400_BAD_REQUEST)

            book_reader = BookReader(book=book, reader=reader, start_date=date.today())
            book_reader.save()

            book_hall.count -= 1
            book_hall.save()

            return Response({"detail": "Book rented successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookAPIView(APIView):
    def post(self, request):
        serializer = BookReaderRequestSerializer(data=request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book']
            reader_id = serializer.validated_data['reader']

            try:
                book = Book.objects.get(id=book_id)
                reader = Reader.objects.get(id=reader_id)
            except (Book.DoesNotExist, Reader.DoesNotExist):
                return Response({"detail": "Book or Reader not found"}, status=status.HTTP_404_NOT_FOUND)

            hall = reader.hall

            book_hall = BookHall.objects.filter(book=book, hall=hall).first()

            if not book_hall:
                return Response({"detail": "Book not available in this hall"}, status=status.HTTP_400_BAD_REQUEST)

            book_reader = BookReader.objects.filter(book=book, reader=reader, end_date=None).first()
            if not book_reader:
                return Response({"detail": "Reader doesn't have this book"}, status=status.HTTP_400_BAD_REQUEST)

            book_reader.end_date = date.today()
            book_reader.save()

            book_hall.count += 1
            book_hall.save()

            return Response({"detail": "Book returned successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddBookAPIView(APIView):
    def post(self, request):
        serializer = AddBookRequestSerializer(data=request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book']
            hall_id = serializer.validated_data['hall']
            amount = serializer.validated_data['amount'] if 'amount' in serializer.validated_data else 1

            try:
                book = Book.objects.get(id=book_id)
                hall = Hall.objects.get(id=hall_id)
            except (Book.DoesNotExist, Hall.DoesNotExist):
                return Response({"detail": "Book or Hall not found"}, status=status.HTTP_404_NOT_FOUND)

            book_hall = BookHall.objects.filter(book=book, hall=hall).first()
            if not book_hall:
                book_hall = BookHall(book=book, hall=hall, count=amount)
            else:
                book_hall.count += amount
            book_hall.save()

            return Response({"detail": "Book added successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveBookAPIView(APIView):
    def post(self, request):
        serializer = AddBookRequestSerializer(data=request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book']
            hall_id = serializer.validated_data['hall']
            amount = serializer.validated_data['amount'] if 'amount' in serializer.validated_data else 1

            try:
                book = Book.objects.get(id=book_id)
                hall = Hall.objects.get(id=hall_id)
            except (Book.DoesNotExist, Hall.DoesNotExist):
                return Response({"detail": "Book or Hall not found"}, status=status.HTTP_404_NOT_FOUND)

            book_hall = BookHall.objects.filter(book=book, hall=hall).first()

            if not book_hall:
                return Response({"detail": "Book not available in this hall"}, status=status.HTTP_400_BAD_REQUEST)

            book_hall.count -= amount
            if book_hall.count <= 0:
                book_hall.delete()
            else:
                book_hall.save()

            return Response({"detail": "Book removed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
