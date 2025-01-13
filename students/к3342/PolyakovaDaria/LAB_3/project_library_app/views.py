from calendar import monthrange
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ReadingRoom, Book, BookCopy, Reader, BookTransaction, ReadingRoomVisit
from .serializers import (
    ReadingRoomSerializer, BookSerializer,
    ReaderSerializer, BookTransactionSerializer
)


class ReadingRoomAPIView(APIView):
    """
    Эндпоинт для управления читальными залами.
    GET: Получение списка всех залов.
    POST: Добавление нового читального зала.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = ReadingRoom.objects.all()
        serializer = ReadingRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(APIView):
    """
    Эндпоинт для управления книгами.
    GET: Получение списка всех книг.
    POST: Добавление новой книги.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """
    Эндпоинт для управления конкретной книгой.
    GET: Получение информации о книге по ID.
    PATCH: Частичное обновление информации о книге.
    DELETE: Удаление книги.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"success": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)


class ManageBookCopiesAPIView(APIView):
    """
    Эндпоинт для управления экземплярами книг.
    GET: Получение информации о количестве экземпляров книги в разных залах.
    POST: Добавление экземпляров книги в зал.
    DELETE: Удаление экземпляров книги из зала.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            book_copies = BookCopy.objects.filter(book=book)
            data = [
                {"room": copy.room.name, "quantity": copy.quantity} for copy in book_copies
            ]
            return Response({"book": book.title, "copies": data})
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)

    def post(self, request, book_id):
        quantity = request.data.get('quantity', 0)
        room_id = request.data.get('room_id')

        if not room_id or not quantity:
            return Response({"error": "Room ID and quantity are required."}, status=400)

        try:
            book = Book.objects.get(pk=book_id)
            room = ReadingRoom.objects.get(pk=room_id)

            book_copy, created = BookCopy.objects.get_or_create(
                book=book,
                room=room,
                defaults={"quantity": 0}
            )
            book_copy.quantity += int(quantity)
            book_copy.save()

            return Response({"success": f"Added {quantity} copies of '{book.title}' to room {room.name}."})
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)
        except ReadingRoom.DoesNotExist:
            return Response({"error": "Reading room not found."}, status=404)

    def delete(self, request, book_id):
        quantity = request.data.get('quantity', 0)
        room_id = request.data.get('room_id')

        if not room_id or not quantity:
            return Response({"error": "Room ID and quantity are required."}, status=400)

        try:
            book = Book.objects.get(pk=book_id)
            room = ReadingRoom.objects.get(pk=room_id)

            book_copy = BookCopy.objects.get(book=book, room=room)
            if book_copy.quantity < int(quantity):
                return Response({"error": f"Cannot remove {quantity} copies. Only {book_copy.quantity} available."}, status=400)

            book_copy.quantity -= int(quantity)
            if book_copy.quantity == 0:
                book_copy.delete()
            else:
                book_copy.save()

            return Response({"success": f"Removed {quantity} copies of '{book.title}' from room {room.name}."})
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)
        except ReadingRoom.DoesNotExist:
            return Response({"error": "Reading room not found."}, status=404)
        except BookCopy.DoesNotExist:
            return Response({"error": "Book copy not found in this room."}, status=404)


class ReaderAPIView(APIView):
    """
    Эндпоинт для управления читателями.
    GET: Получение списка всех читателей.
    POST: Добавление нового читателя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        readers = Reader.objects.all()
        serializer = ReaderSerializer(readers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookTransactionListCreateAPIView(APIView):
    """
    Эндпоинт для управления транзакциями с книгами.
    GET: Получение списка всех транзакций.
    POST: Добавление новой транзакции.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = BookTransaction.objects.all()
        serializer = BookTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookTransactionDetailAPIView(APIView):
    """
    Эндпоинт для управления конкретной транзакцией.
    GET: Получение информации о транзакции по ID.
    PATCH: Обновление транзакции (например, отметка о возврате книги).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            transaction = BookTransaction.objects.get(pk=pk)
            serializer = BookTransactionSerializer(transaction)
            return Response(serializer.data)
        except BookTransaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            transaction = BookTransaction.objects.get(pk=pk)
            transaction.returned = True
            transaction.save()
            return Response({"success": f"Book '{transaction.book.title}' marked as returned."},
                            status=status.HTTP_200_OK)
        except BookTransaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)


class ReaderBooksAPIView(APIView):
    """
    Эндпоинт для получения книг, закрепленных за читателем.
    GET: Возвращает список книг, выданных конкретному читателю.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, reader_id):
        transactions = BookTransaction.objects.filter(reader_id=reader_id, returned=False)
        serializer = BookTransactionSerializer(transactions, many=True)
        return Response({"books_assigned_to_reader": serializer.data})


class LateBooksAPIView(APIView):
    """
    Эндпоинт для получения списка просроченных книг.
    GET: Возвращает список книг, выданных более месяца назад и не возвращенных.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        one_month_ago = timezone.now() - timedelta(days=30)
        overdue_transactions = BookTransaction.objects.filter(
            transaction_type="Выдача",
            transaction_date__lte=one_month_ago,
            returned=False
        )
        serializer = BookTransactionSerializer(overdue_transactions, many=True)
        return Response({"overdue_books": serializer.data})


class RemoveOldReadersAPIView(APIView):
    """
    Эндпоинт для управления старыми читателями.
    GET: Возвращает список читателей, которые могут быть удалены.
    DELETE: Удаляет читателей, которые зарегистрировались более года назад и не перерегистрировались.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        one_year_ago = timezone.now() - timedelta(days=365)
        old_readers = Reader.objects.filter(
            registration_date__lte=one_year_ago,
            re_registered=False
        )
        readers_data = old_readers.values(
            "id", "full_name", "registration_date", "re_registered"
        )
        return Response({"potentially_removable_readers": list(readers_data)})

    def delete(self, request):
        one_year_ago = timezone.now() - timedelta(days=365)
        old_readers = Reader.objects.filter(
            registration_date__lte=one_year_ago,
            re_registered=False
        )
        count = old_readers.count()
        old_readers.delete()
        return Response({"removed_readers_count": count})


class LibraryReportAPIView(APIView):
    """
    Эндпоинт для генерации отчетов о библиотеке.
    GET: Генерация отчета о книгах, залах, новых читателях.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report_type = request.query_params.get('report_type')
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', 0))

        if report_type == "monthly":
            if month:
                start_date = datetime(year, month, 1)
                end_date = start_date + timedelta(days=monthrange(year, month)[1] - 1)
            else:
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31)

            room_data = ReadingRoomVisit.objects.filter(
                visit_date__range=(start_date, end_date)
            ).values("room__name").annotate(count=Count("reader")).order_by("room__name")

            book_count = Book.objects.aggregate(total=Count('id'))

            new_readers = Reader.objects.filter(
                registration_date__range=(start_date, end_date)
            ).count()

            return Response({
                "room_data": room_data,
                "total_books": book_count,
                "new_readers": new_readers
            })

        elif report_type == "reader_statistics":
            age_limit = timezone.now().year - 20
            readers_under_20 = Reader.objects.filter(birth_date__year__gte=age_limit).count()

            total_readers = Reader.objects.count()
            education_stats = {}
            if total_readers > 0:
                education_levels = Reader.objects.values('education_level').annotate(count=Count('id'))
                education_stats = {
                    level['education_level']: round((level['count'] / total_readers) * 100, 2)
                    for level in education_levels
                }

            return Response({
                "readers_under_20": readers_under_20,
                "education_statistics": education_stats
            })

        return Response({"error": "Invalid report type."}, status=status.HTTP_400_BAD_REQUEST)


class TransferBookAPIView(APIView):
    """
    Эндпоинт для перемещения экземпляра книги в другой зал.
    GET: Возвращает информацию о текущем зале экземпляра книги.
    POST: Указывает, в какой зал перенести экземпляр книги.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, book_copy_id):
        try:
            book_copy = BookCopy.objects.get(id=book_copy_id)
            room = book_copy.room
            return Response({
                "book_copy_id": book_copy_id,
                "current_room_id": room.id,
                "current_room_name": room.name
            })
        except BookCopy.DoesNotExist:
            return Response({"error": "Book copy not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, book_copy_id):
        room_id = request.data.get('room_id')
        try:
            book_copy = BookCopy.objects.get(id=book_copy_id)
            book_copy.room_id = room_id
            book_copy.save()
            return Response({"success": f"Book copy transferred to room {room_id}."})
        except BookCopy.DoesNotExist:
            return Response({"error": "Book copy not found."}, status=status.HTTP_404_NOT_FOUND)



class ComplexLibraryReportAPIView(APIView):
    """
    Эндпоинт для генерации сложных отчетов о библиотеке.
    GET: Возвращает данные по читателям, книгам и залам.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report_type = request.query_params.get('report_type')

        if report_type == "summary":
            month = int(request.query_params.get('month', timezone.now().month))
            year = int(request.query_params.get('year', timezone.now().year))
            start_date = datetime(year, month, 1)
            end_date = start_date + timedelta(days=monthrange(year, month)[1] - 1)

            readers_under_20 = Reader.objects.filter(birth_date__year__gte=timezone.now().year - 20).count()

            total_readers = Reader.objects.count()
            education_levels = Reader.objects.values('education_level').annotate(count=Count('id'))
            education_stats = {
                level['education_level']: round((level['count'] / total_readers) * 100, 2)
                for level in education_levels
            } if total_readers > 0 else {}

            room_data = ReadingRoomVisit.objects.filter(
                visit_date__range=(start_date, end_date)
            ).values("room__name").annotate(count=Count("reader")).order_by("room__name")

            book_count = Book.objects.aggregate(total=Count('id'))

            return Response({
                "readers_under_20": readers_under_20,
                "education_statistics": education_stats,
                "room_data": room_data,
                "total_books": book_count
            })

        return Response({"error": "Invalid report type."}, status=status.HTTP_400_BAD_REQUEST)


class TransferReaderAPIView(APIView):
    """
    Эндпоинт для перемещения читателя в другой зал.
    POST: Указывает зал, в который нужно переместить читателя.
    GET: Получение информации о текущем зале читателя.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, reader_id):
        room_id = request.data.get("room_id")

        if not room_id:
            return Response({"error": "Room ID is required."}, status=400)

        try:
            reader = Reader.objects.get(pk=reader_id)
            room = ReadingRoom.objects.get(pk=room_id)

            reader.assigned_room = room
            reader.save()

            return Response({"success": f"Reader '{reader.full_name}' transferred to room '{room.name}'."})
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=404)
        except ReadingRoom.DoesNotExist:
            return Response({"error": "Reading room not found."}, status=404)

    def get(self, request, reader_id):
        try:
            reader = Reader.objects.get(pk=reader_id)
            room = reader.assigned_room
            room_name = room.name if room else "No room assigned"

            return Response({
                "reader": reader.full_name,
                "assigned_room": room_name
            })
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=404)


class ReadingRoomReadersAPIView(APIView):
    """
    Эндпоинт для получения списка читателей в зале.
    GET: Возвращает список читателей, закрепленных за залом.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ReadingRoom.objects.get(pk=room_id)
            readers = Reader.objects.filter(assigned_room=room)
            serializer = ReaderSerializer(readers, many=True)
            return Response({"room": room.name, "readers": serializer.data})
        except ReadingRoom.DoesNotExist:
            return Response({"error": "Reading room not found."}, status=404)


class UpdateBookCodeAPIView(APIView):
    """
    Эндпоинт для обновления шифра книги.
    GET: Получение текущего шифра книги.
    PATCH: Обновление шифра книги.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            return Response({
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "current_code": book.code
                }
            }, status=200)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)

    def patch(self, request, book_id):
        new_code = request.data.get("new_code")

        if not new_code:
            return Response({"error": "New code is required."}, status=400)

        try:
            book = Book.objects.get(pk=book_id)
            book.code = new_code
            book.save()

            return Response({
                "success": f"Book code updated successfully.",
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "new_code": book.code
                }
            }, status=200)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=404)


class UpdateReaderTicketAPIView(APIView):
    """
    Эндпоинт для обновления номера читательского билета.
    GET: Получение текущего номера билета.
    PATCH: Обновление номера билета.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, reader_id):
        try:
            reader = Reader.objects.get(pk=reader_id)
            return Response({
                "reader": {
                    "id": reader.id,
                    "full_name": reader.full_name,
                    "current_ticket_number": reader.ticket_number
                }
            }, status=200)
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=404)

    def patch(self, request, reader_id):
        new_ticket_number = request.data.get("new_ticket_number")

        if not new_ticket_number:
            return Response({"error": "New ticket number is required."}, status=400)

        try:
            reader = Reader.objects.get(pk=reader_id)

            if Reader.objects.filter(ticket_number=new_ticket_number).exists():
                return Response({"error": "This ticket number is already in use."}, status=400)

            reader.ticket_number = new_ticket_number
            reader.save()

            return Response({
                "success": "Reader ticket number updated successfully.",
                "reader": {
                    "id": reader.id,
                    "full_name": reader.full_name,
                    "new_ticket_number": reader.ticket_number
                }
            }, status=200)
        except Reader.DoesNotExist:
            return Response({"error": "Reader not found."}, status=404)


class LowStockBooksAPIView(APIView):
    """
    Эндпоинт для получения списка книг с низким количеством экземпляров.
    GET: Возвращает книги с количеством <= 2 и читателей, которые их взяли.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            low_stock_books = (
                BookCopy.objects
                .values("book")
                .annotate(total_quantity=Count("id"), sum_quantity=Sum("quantity"))
                .filter(sum_quantity__lte=2)
            )

            book_ids = [entry["book"] for entry in low_stock_books]
            books = Book.objects.filter(id__in=book_ids)

            book_transactions = BookTransaction.objects.filter(
                book_id__in=book_ids, returned=False
            ).select_related("reader", "book")

            result = []
            for book in books:
                readers = [
                    {
                        "id": transaction.reader.id,
                        "full_name": transaction.reader.full_name,
                        "ticket_number": transaction.reader.ticket_number,
                    }
                    for transaction in book_transactions if transaction.book_id == book.id
                ]
                result.append({
                    "book": {
                        "id": book.id,
                        "title": book.title,
                        "authors": book.authors,
                        "current_code": book.code,
                    },
                    "readers": readers
                })

            return Response(result, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)