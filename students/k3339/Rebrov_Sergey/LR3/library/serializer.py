from .models import *
from rest_framework import serializers


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "year"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "surname", "name", "patronymic"]


class BookReadSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'publisher', 'cipher', 'authors']

    def get_authors(self, obj):
        # Получаем всех авторов через промежуточную модель
        authors = Author.objects.filter(bookauthor__book=obj)
        return AuthorSerializer(authors, many=True).data


class BookWriteSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(), write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'name', 'publisher', 'cipher', 'authors']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        BookAuthor.objects.bulk_create([
            BookAuthor(book=book, author=author) for author in authors_data
        ])
        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        if authors_data is not None:
            BookAuthor.objects.filter(book=instance).delete()
            BookAuthor.objects.bulk_create([
                BookAuthor(book=instance, author=author) for author in authors_data
            ])
        return super().update(instance, validated_data)


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "name", "address"]


class HallReadSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()

    class Meta:
        model = Hall
        fields = ["id", "number", "name", "capacity", "library"]


class HallWriteSerializer(serializers.ModelSerializer):
    library = serializers.PrimaryKeyRelatedField(queryset=Library.objects.all())

    class Meta:
        model = Hall
        fields = ["id", "number", "name", "capacity", "library"]

    def update(self, instance, validated_data):
        library_data = validated_data.pop('library', None)

        if library_data:
            instance.library = Library.objects.get(id=library_data.id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ReaderReadSerializer(serializers.ModelSerializer):
    hall = HallReadSerializer()

    class Meta:
        model = Reader
        fields = ["id", "surname", "name", "patronymic", "ticket", "passport", "birth_date", "address", "phone", "education", "is_academic", "hall"]


class ReaderWriteSerializer(serializers.ModelSerializer):
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())

    class Meta:
        model = Reader
        fields = ["id", "surname", "name", "patronymic", "ticket", "passport", "birth_date", "address", "phone", "education", "is_academic", "hall"]

    def update(self, instance, validated_data):
        hall_data = validated_data.pop('hall', None)

        if hall_data:
            instance.hall = Hall.objects.get(id=hall_data.id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class BookReaderRequestSerializer(serializers.Serializer):
    book = serializers.IntegerField()
    reader = serializers.IntegerField()


class AddBookRequestSerializer(serializers.Serializer):
    book = serializers.IntegerField()
    hall = serializers.IntegerField()
    amount = serializers.IntegerField(required=False, min_value=1)
