from datetime import date, timedelta
from rest_framework import generics
from rest_framework.views import Response, APIView, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count
from .serializers import *
from .models import *

class GenreListView(generics.ListAPIView):
    serializer_class = GenreSerializer
    permission_classes=[IsAuthenticated]
    queryset = Genre.objects.all()

class GenreCreateView(generics.CreateAPIView):
    serializer_class = GenreSerializer
    permission_classes=[IsAuthenticated]

class GenreRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    permission_classes=[IsAuthenticated]
    queryset = Genre.objects.all()

class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes=[IsAuthenticated]
    queryset = Author.objects.all()

class AuthorCreateView(generics.CreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes=[IsAuthenticated]

class AuthorRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    permission_classes=[IsAuthenticated]
    queryset = Author.objects.all()

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()

class BookCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes=[IsAuthenticated]

class BookRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes=[IsAuthenticated]
    queryset = Book.objects.all()

class BookCopyListView(generics.ListAPIView):
    serializer_class = BookCopySerializer
    permission_classes=[IsAuthenticated]
    queryset = BookCopy.objects.all()

class BookCopyCreateView(generics.CreateAPIView):
    serializer_class = BookCopySerializer
    permission_classes=[IsAuthenticated]

class BookCopyRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookCopySerializer
    permission_classes=[IsAuthenticated]
    queryset = BookCopy.objects.all()

class ReaderListView(generics.ListAPIView):
    serializer_class = ReaderSerializer
    permission_classes=[IsAuthenticated]
    queryset = Reader.objects.all()

class ReaderCreateView(generics.CreateAPIView):
    serializer_class = ReaderSerializer
    permission_classes=[IsAuthenticated]

class ReaderRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReaderSerializer
    permission_classes=[IsAuthenticated]
    queryset = Reader.objects.all()

class ReadingRoomListView(generics.ListAPIView):
    serializer_class = ReadingRoomSerializer
    permission_classes=[IsAuthenticated]
    queryset = ReadingRoom.objects.all()

class ReadingRoomCreateView(generics.CreateAPIView):
    serializer_class = ReadingRoomSerializer
    permission_classes=[IsAuthenticated]

class ReadingRoomRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReadingRoomSerializer
    permission_classes=[IsAuthenticated]
    queryset = ReadingRoom.objects.all()

class BookTakeCreateView(generics.CreateAPIView):
    serializer_class = BookTakeSerializer
    permission_classes=[IsAuthenticated]

class BookTakeRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookTakeSerializer
    permission_classes=[IsAuthenticated]
    queryset = BookTake.objects.all()

class ReaderBooksView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, **kwargs):
        try:
            reader = Reader.objects.get(id=kwargs['pk'])
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=status.HTTP_404_NOT_FOUND)

        book_takes = BookTake.objects.filter(reader=reader, restore_date__isnull=True)
        serializer = BookTakeSerializer(book_takes, many=True)

        return Response(serializer.data)

class ReadersMonthDelayView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, **kwargs):
        last_month_date = date.today() - timedelta(days=30)
        delayed_takes = BookTake.objects.filter(take_date__lt=last_month_date, restore_date__isnull=True)
        serializer = BookTakeReaderSerializer(delayed_takes, many=True)

        return Response(serializer.data)

class ReadersLessThanBooksView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, **kwargs):
        books_pks = BookCopy.objects \
                            .values('book').annotate(Count('id')) \
                            .filter(id__count__lt=5).values_list('book', flat=True)
        book_takes = BookTake.objects.filter(book_copy__book__id__in=books_pks, restore_date__isnull=True)
        serializer = BookTakeReaderSerializer(book_takes, many=True)

        return Response(serializer.data)

class ReadersLessTwentyYears(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, **kwargs):
        date_ago = date.today() - timedelta(days=(20*365))
        readers = Reader.objects.filter(birthdate__gt=date_ago)
        count = len(readers)
        serializer = ReaderSerializer(readers, many=True)

        return Response({'count':count, 'readers':serializer.data})
    
class ReadersEducationPercentageView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        total_readers = Reader.objects.count()
        if total_readers == 0:
            return Response({"message": "Нет данных о читателях."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "total": total_readers,
            "начальное": round(Reader.objects.filter(education='н').count() / total_readers, 2),
            "среднее": round(Reader.objects.filter(education='с').count() / total_readers, 2),
            "высшее": round(Reader.objects.filter(education='в').count() / total_readers, 2),
            "учёная степень": round(Reader.objects.filter(degree=True).count() / total_readers, 2)
        }

        return Response(data)
