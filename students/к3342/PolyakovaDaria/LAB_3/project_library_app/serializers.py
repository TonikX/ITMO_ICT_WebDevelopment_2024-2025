from rest_framework import serializers
from .models import ReadingRoom, Book, BookCopy, Reader, BookTransaction, ReadingRoomVisit


class ReadingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoom
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = "__all__"


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = "__all__"


class BookTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTransaction
        fields = "__all__"


class ReadingRoomVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoomVisit
        fields = "__all__"
