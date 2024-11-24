import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from library_app.serializers import *
from library_app.models import *

from library_app.serializers import BookTakeSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class ReadingRoomViewSet(ModelViewSet):
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["GET"])
    def show_readers(self, request, pk=None):
        obj = self.get_object()
        qs = Reader.objects.filter(reading_room=obj.id)
        ser = self.get_serializer(qs, many=True)
        return ser.data


class ReaderViewSet(ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def show_taken(self, request, pk=None):
        obj = self.get_object()
        qs = BookTake.objects.filter(reader=obj.id)
        ser = BookTakeSerializer(qs, many=True)
        return Response(ser.data)

    @action(detail=False, methods=['GET'])
    def youngest(self, request):
        date = datetime.date.today() - datetime.timedelta(days=(365*20))
        ser = self.get_serializer(self.queryset.filter(birth_date__gt=date), many=True)
        return Response(ser.data)

    @action(detail=False, methods=['GET'])
    def percentage(self, request):
        data = {
            'всего': self.queryset.count(),
            "начальное": self.queryset.filter(education='н').count(),
            "среднее": self.queryset.filter(education='с').count(),
            "высшее": self.queryset.filter(education='в').count(),
        }
        return Response(data)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return ShowBookSerializer
        return BookSerializer

    @action(detail=False, methods=['GET'])
    def take_unique_books(self, request):
        res_qs = BookTake.objects.none()
        for obj in self.queryset:
            count = BookCopy.objects.filter(book=obj.id).count()
            if count <= 2:
                res_qs |= BookTake.objects.filter(book_copy__book=obj.id)
        return Response(ShowBookTakeSerializer(res_qs, many=True).data)


class BookCopyViewSet(ModelViewSet):
    queryset = BookCopy.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return ShowBookCopySerializer
        return BookCopySerializer


class BookTakeViewSet(ModelViewSet):
    queryset = BookTake.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return ShowBookTakeSerializer
        return BookTakeSerializer

    @action(detail=False, methods=['GET'])
    def take_last_month(self, request):
        date = datetime.date.today() - datetime.timedelta(weeks=4)
        qs = self.queryset.filter(take_date__gte=date)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

