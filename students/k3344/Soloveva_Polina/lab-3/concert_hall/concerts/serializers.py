from rest_framework import serializers
from .models import Concert, Ticket, Order, Organizer, ConcertEquipment, Equipment


# --- Пользователи ---
class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)


# --- Концерты ---
class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['title', 'performer', 'description', 'date', 'age_limit']


class ConcertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['id', 'title', 'date']


class ConcertDetailSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = ['id', 'title', 'description', 'date', 'age_limit', 'status', 'performer', 'tickets']

    def get_tickets(self, obj):
        return TicketDetailSerializer(obj.ticket_categories.all(), many=True).data


# --- Билеты ---
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'price', 'total_quantity', 'concert']


class TicketDetailSerializer(serializers.ModelSerializer):
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'price', 'total_quantity', 'sold_quantity', 'available_quantity']

    def get_available_quantity(self, obj):
        return obj.total_quantity - obj.sold_quantity


class TicketCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()


class TicketOrderSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ['name', 'price', 'concert']


# --- Заказы ---
class OrderSerializer(serializers.ModelSerializer):
    ticket = TicketOrderSerializer()

    class Meta:
        model = Order
        fields = ['ticket', 'quantity', 'date', 'total_price', 'status']


class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['ticket', 'quantity']

    def create(self, validated_data):
        ticket = validated_data['ticket']
        quantity = validated_data['quantity']

        # Проверяем, есть ли достаточно билетов
        if ticket.available_quantity < quantity:
            raise serializers.ValidationError({"error": "Недостаточно доступных билетов"})

        # Обновляем количество проданных билетов
        ticket.sell_tickets(quantity)

        # Создаем заказ
        order = Order.objects.create(**validated_data)
        return order


# --- Организаторы ---
class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'


# --- Оборудование ---
class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name']


class ConcertEquipmentSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = ConcertEquipment
        fields = ['concert', 'equipment', 'quantity']


class ConcertEquipmentCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertEquipment
        fields = ['concert', 'equipment', 'quantity']
