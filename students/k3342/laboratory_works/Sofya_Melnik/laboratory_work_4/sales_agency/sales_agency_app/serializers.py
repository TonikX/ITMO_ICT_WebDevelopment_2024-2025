from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Service, PriceList, Position, Employee, PositionEmployee, Order, PaymentOrder


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    contact_person = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "re_password", "phone", "first_name", "last_name", "contact_person")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get("password") != data.get("re_password"):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        print("Сериализатор: начинаем создание пользователя и клиента")

        contact_person = validated_data.pop('contact_person', None)
        phone = validated_data.pop('phone', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        

        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        print("Создан пользователь:", user)
        client = Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            contact_person=contact_person,
            email=validated_data.get("email"),
            phone=phone
        )

        print("Создан клиент:", client)
        return user
    
#User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')


#Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'contact_person', 'email', 'phone']


#Service
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


#PriceList
class PriceListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )

    class Meta:
        model = PriceList
        fields = ['id', 'service', 'service_id', 'price', 'start_price', 'end_price']

    def validate(self, data):
        if data['start_price'] >= data['end_price']:
            raise serializers.ValidationError("Дата начала действия цены должна быть раньше даты окончания.")
        return data
    
    def create(self, validated_data):
        return PriceList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


#Position
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


#Employee
class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), write_only=True
    )
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'position', 'position_id', 'order_count']

    def create(self, validated_data):
        position = validated_data.pop('position_id', None)
        employee = Employee.objects.create(position=position, **validated_data)
        return employee

    def update(self, instance, validated_data):
        position = validated_data.pop('position_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if position is not None:
            instance.position = position
        instance.save()
        return instance

    
    def get_order_count(self, obj):
        # Подсчитываем количество заявок у этого сотрудника для отчета
        return Order.objects.filter(employee=obj, status='completed').count()

#PositionEmployee
class PositionEmployeeSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True
    )
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), write_only=True
    )

    class Meta:
        model = PositionEmployee
        fields = ['id', 'employee', 'employee_id', 'position', 'position_id', 'start_date', 'end_date']
    
    def create(self, validated_data):
        employee = validated_data.pop('employee_id', None)
        position = validated_data.pop('position_id')
        position_employee = PositionEmployee.objects.create(employee=employee, position=position, **validated_data)
        return position_employee


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), write_only=True
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_id', 'service', 'service_id', 'employee', 'employee_id',
            'order_date', 'completion_date', 'quantity', 'total_cost', 'status'
        ]

    def validate(self, data):
        if data.get('completion_date') and data.get('order_date'):
            if data['completion_date'] < data['order_date']:
                raise serializers.ValidationError("Дата завершения заказа не может быть раньше даты создания.")
        
        if data.get('quantity') and data['quantity'] <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0.")
        
        return data

    def create(self, validated_data):
        client = validated_data.pop('client_id')
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id')
        order_date = validated_data.get('order_date')
        completion_date = validated_data.get('completion_date')
        quantity = validated_data.get('quantity')
        total_cost = validated_data.get('total_cost')
        status = validated_data.get('status')

        order = Order.objects.create(
            client=client,
            service=service,
            employee=employee,
            order_date=order_date,
            completion_date=completion_date,
            quantity=quantity,
            total_cost=total_cost,
            status=status
        )
        return order

    def update(self, instance, validated_data):
        if 'client_id' in validated_data:
            raise serializers.ValidationError("Client cannot be changed.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

#PaymentOrder
class PaymentOrderSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = PaymentOrder
        fields = '__all__'