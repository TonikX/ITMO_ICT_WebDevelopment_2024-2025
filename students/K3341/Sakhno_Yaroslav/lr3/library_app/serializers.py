from rest_framework import serializers
from library_app.models import (Category,
                                Author,
                                ReadingRoom,
                                BookTake,
                                Reader,
                                Book,
                                BookCopy)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ReadingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoom
        fields = "__all__"


class ReaderSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(read_only=True, many=True, slug_field='books')

    class Meta:
        model = Reader
        fields = "__all__"

####################################


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ShowBookSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True, read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['name', 'publisher', 'category', 'authors']


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = "__all__"


class ShowBookCopySerializer(serializers.ModelSerializer):
    book = ShowBookSerializer(read_only=True)

    class Meta:
        model = BookCopy
        fields = ['book', 'cipher', 'publishing_year']


class BookTakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTake
        fields = '__all__'


class ShowBookTakeSerializer(serializers.ModelSerializer):
    book_copy = ShowBookCopySerializer(read_only=True)
    reader = ReaderSerializer(read_only=True)

    class Meta:
        model = BookTake
        fields = ['book_copy', 'reader', 'take_date', 'return_date']