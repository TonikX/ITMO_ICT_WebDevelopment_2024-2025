from rest_framework import serializers
from .models import *

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'publisher')

class BookCopySerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookCopy
        fields = '__all__'

class BookCopyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'

class ReadingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoom
        fields = '__all__'

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'

class ReaderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'

class BookTakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTake
        fields = '__all__'

class ReaderContactInformationSerializer(serializers.ModelSerializer):
    reading_room = ReadingRoomSerializer()
    class Meta:
        model = Reader
        fields = ['full_name', 'reading_room', 'address', 'phone_number', 'reading_ticket_number']

class BookTakeReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTake
        fields = ['reader', 'book_copy', 'take_date']

class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = '__all__'

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = '__all__'
