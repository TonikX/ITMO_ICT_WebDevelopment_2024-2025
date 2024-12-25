from rest_framework import serializers
from .models import (
    Employee, Author, Book, BookAuthor, Edition, Contract,
    EditionEditor, Customer, Order, OrderItem
)

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'



class BookAuthorCreateSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    position_on_cover = serializers.IntegerField()
    royalty_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_author_id(self, value):
        if not Author.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Указанный автор не существует.")
        return value


class BookCreateSerializer(serializers.ModelSerializer):
    authors_data = BookAuthorCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Book
        fields = ['title', 'authors_data']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors_data', [])
        book = Book.objects.create(**validated_data)

        book_authors_bulk = []
        for author_info in authors_data:
            author = Author.objects.get(pk=author_info['author_id'])
            book_authors_bulk.append(
                BookAuthor(
                    book=book,
                    author=author,
                    position_on_cover=author_info['position_on_cover'],
                    royalty_percentage=author_info['royalty_percentage']
                )
            )
        BookAuthor.objects.bulk_create(book_authors_bulk)

        return book

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id
        data['authors'] = [
            {
                'author_id': ba.author.id,
                'first_name': ba.author.first_name,
                'last_name': ba.author.last_name,
                'position_on_cover': ba.position_on_cover,
                'royalty_percentage': str(ba.royalty_percentage)
            } 
            for ba in instance.book_authors.order_by('position_on_cover')
        ]
        return data


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class EditionEditorSerializer(serializers.ModelSerializer):
    editor = EmployeeSerializer(read_only=True)
    editor_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(role=Employee.Role.EDITOR),
        write_only=True,
        source='editor'
    )

    class Meta:
        model = EditionEditor
        fields = ['id', 'editor', 'editor_id', 'is_responsible_editor']

class EditionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'
    )
    editors = EditionEditorSerializer(many=True, source='edition_editors', required=False)

    class Meta:
        model = Edition
        fields = [
            'id',
            'book',
            'book_id',
            'edition_number',
            'publication_date',
            'number_of_pages',
            'has_illustrations',
            'editors',
        ]

    def create(self, validated_data):
        editors_data = validated_data.pop('edition_editors', [])
        edition = Edition.objects.create(**validated_data)
        for editor_data in editors_data:
            EditionEditor.objects.create(edition=edition, **editor_data)
        return edition

    def update(self, instance, validated_data):
        editors_data = validated_data.pop('edition_editors', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if editors_data is not None:
            # Удаление существующих редакторов
            instance.edition_editors.all().delete()
            # Добавление новых редакторов
            for editor_data in editors_data:
                EditionEditor.objects.create(edition=instance, **editor_data)

        return instance

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    edition = EditionSerializer(read_only=True)
    edition_id = serializers.PrimaryKeyRelatedField(
        queryset=Edition.objects.all(),
        write_only=True,
        source='edition'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'edition', 'edition_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        write_only=True,
        source='customer'
    )
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'date_ordered', 'order_items']

    def validate(self, data):
        order_items = data.get('order_items', [])
        edition_ids = [item['edition'].id for item in order_items]
        if len(edition_ids) != len(set(edition_ids)):
            raise serializers.ValidationError("Позиции заказа содержат дублирующиеся издания.")
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        customer = validated_data.pop('customer', None)

        # Обновление полей заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if customer:
            instance.customer = customer
        instance.save()

        if order_items_data is not None:
            # Удаление существующих позиций
            instance.order_items.all().delete()
            # Создание новых позиций
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance