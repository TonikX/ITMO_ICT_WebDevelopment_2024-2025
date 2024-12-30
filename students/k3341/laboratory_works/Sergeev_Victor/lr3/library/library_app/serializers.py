from rest_framework import serializers
from .models import *

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['id']

class BookSerializer(serializers.ModelSerializer):
    # genre = GenreSerializer(many=True)
    # author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publisher']

class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookCopy
        fields = '__all__'

class ReadingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoom
        fields = '__all__'

class ReaderSerializer(serializers.ModelSerializer):
    reading_room = ReadingRoomSerializer()

    class Meta:
        model = Reader
        fields = '__all__'

class BookTakeSerializer(serializers.ModelSerializer):
    book_copy = BookCopySerializer()

    class Meta:
        model = BookTake
        exclude = ['reader']

class ReaderContactInformationSerializer(serializers.ModelSerializer):
    reading_room = ReadingRoomSerializer()
    class Meta:
        model = Reader
        fields = ['full_name', 'reading_room', 'address', 'phone_number', 'reading_ticket_number']

class BookTakeReaderSerializer(serializers.ModelSerializer):
    reader = ReaderContactInformationSerializer()
    book_copy = BookCopySerializer()

    class Meta:
        model = BookTake
        fields = ['reader', 'book_copy', 'take_date']
