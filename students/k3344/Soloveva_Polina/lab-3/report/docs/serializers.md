# Сериализаторы

## Пользователи

### UserRegistrationSerializer
```python
class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
```
- Используется для регистрации пользователя.
- Поля: username, email (необязательное), password (скрытое поле).

### UserLoginSerializer
```python
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
```
- Используется для авторизации пользователя.
- Поля: username, password (скрытое поле).

## Концерты

### ConcertSerializer
```python
class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['title', 'performer', 'description', 'date', 'age_limit']
```
- Используется для создания и обновления концертов.
- Поля: название, исполнитель, описание, дата, возрастное ограничение.

### ConcertListSerializer
```python
class ConcertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['id', 'title', 'date']
```
- Используется для списка концертов.
- Поля: ID, название, дата.

### ConcertDetailSerializer
```python
class ConcertDetailSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Concert
        fields = ['id', 'title', 'description', 'date', 'age_limit', 'status', 'performer', 'tickets']

    def get_tickets(self, obj):
        return TicketDetailSerializer(obj.ticket_categories.all(), many=True).data
```
- Используется для детальной информации о концерте.
- Включает связанные билеты.

## Билеты

### TicketSerializer
```python
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'price', 'total_quantity', 'concert']
```
- Используется для создания и обновления билетов.
- Поля: название, цена, общее количество, связанный концерт.

### TicketDetailSerializer
```python
class TicketDetailSerializer(serializers.ModelSerializer):
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'price', 'total_quantity', 'sold_quantity', 'available_quantity']

    def get_available_quantity(self, obj):
        return obj.total_quantity - obj.sold_quantity
```
- Используется для просмотра билетов.
- Рассчитывает доступное количество билетов.

### TicketCreateSerializer
```python
class TicketCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
```
- Используется для создания билетов.
- Поля: название, цена, количество.

### TicketOrderSerializer
```python
class TicketOrderSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['name', 'price', 'concert']
```
- Используется для отображения информации о заказе билета.
- Включает связанные концерты.

## Заказы

### OrderSerializer
```python
class OrderSerializer(serializers.ModelSerializer):
    ticket = TicketOrderSerializer()

    class Meta:
        model = Order
        fields = ['ticket', 'quantity', 'date', 'total_price', 'status']
```
- Используется для просмотра заказов.
- Включает информацию о билете и статусе заказа.

### OrderCreationSerializer
```python
class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['ticket', 'quantity']

    def create(self, validated_data):
        ticket = validated_data['ticket']
        quantity = validated_data['quantity']

        if ticket.available_quantity < quantity:
            raise serializers.ValidationError({"error": "Недостаточно доступных билетов"})

        ticket.sell_tickets(quantity)
        order = Order.objects.create(**validated_data)
        return order
```
- Используется для создания заказа.
- Проверяет наличие билетов перед созданием заказа.

## Организаторы

### OrganizerSerializer
```python
class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
```
- Используется для сериализации организаторов концертов.
- Включает все поля модели.

## Оборудование

### EquipmentSerializer
```python
class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name']
```
- Используется для списка оборудования.
- Поля: название оборудования.

### ConcertEquipmentSerializer
```python
class ConcertEquipmentSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = ConcertEquipment
        fields = ['concert', 'equipment', 'quantity']
```
- Используется для отображения оборудования, связанного с концертом.
- Включает информацию о концерте и количестве оборудования.

### ConcertEquipmentCreationSerializer
```python
class ConcertEquipmentCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertEquipment
        fields = ['concert', 'equipment', 'quantity']
```
- Используется для добавления оборудования к концерту.
- Поля: концерт, оборудование, количество.

