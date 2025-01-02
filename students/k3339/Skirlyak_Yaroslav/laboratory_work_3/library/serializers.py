from rest_framework import serializers
from .models import Book, Author, Reader, ReadingRoom, BookAssignment, BookRoom


class AuthorSerializer(serializers.ModelSerializer):
    num_books = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'num_books']


class ReadingRoomSerializer(serializers.ModelSerializer):
    num_readers = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReadingRoom
        fields = ['id', 'name', 'capacity', 'num_readers']


class BookRoomSerializer(serializers.ModelSerializer):
    room = ReadingRoomSerializer()

    class Meta:
        model = BookRoom
        fields = ['room', 'copy_id']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    rooms = BookRoomSerializer(source='bookroom_set', many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'book_code', 'title', 'publisher', 'year_of_publication',
            'section', 'authors', 'rooms'
        ]


class BookAssignmentSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    date_assigned = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = BookAssignment
        fields = ['book', 'date_assigned']


class ReaderSerializer(serializers.ModelSerializer):
    current_room = ReadingRoomSerializer(read_only=True)
    assigned_books = BookAssignmentSerializer(source='assignment_set', many=True, read_only=True)

    class Meta:
        model = Reader
        fields = [
            'id', 'reader_card_number', 'full_name', 'passport_number',
            'date_of_birth', 'address', 'phone_number', 'education',
            'academic_degree', 'current_room', 'registration_date',
            'is_active', 'assigned_books'
        ]