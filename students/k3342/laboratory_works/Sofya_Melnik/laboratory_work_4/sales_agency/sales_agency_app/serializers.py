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
        first_name = validated_data.pop('first_name', None)  # Извлекаем имя (если передано)
        last_name = validated_data.pop('last_name', None)  # Извлекаем фамилию (если передано)

        # Создаем пользователя
        password = validated_data.pop('password')  # Обрабатываем пароль отдельно
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Устанавливаем пароль
        user.save()
        print("Создан пользователь:", user)
        # Создаем клиента на основе данных регистрации (связь через email, например)
        client = Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            contact_person=contact_person,
            email=validated_data.get("email"),
            phone=phone
        )

        print("Создан клиент:", client)
        return user
    
# --- User ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')


# --- Client ---
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'contact_person', 'email', 'phone']


# --- Service ---
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


# --- PriceList ---
class PriceListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)  # Показываем вложенный объект услуги
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )  # Оставляем возможность передавать ID

    class Meta:
        model = PriceList
        fields = ['id', 'service', 'service_id', 'price', 'start_price', 'end_price']

    def validate(self, data):
        """ Проверяем, что дата начала меньше даты окончания """
        if data['start_price'] >= data['end_price']:
            raise serializers.ValidationError("Дата начала действия цены должна быть раньше даты окончания.")
        return data
    
    def create(self, validated_data):
        """ Создание объекта PriceList """
        return PriceList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ Обновление объекта PriceList """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# --- Position ---
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


# --- Employee ---
class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)  # Для вывода информации о позиции
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), write_only=True  # Для получения ID позиции
    )
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'position', 'position_id', 'order_count']

    def create(self, validated_data):
        # Получаем ID позиции и удаляем его из словаря
        position = validated_data.pop('position_id', None)
        # Создаем сотрудника, передавая ID позиции в нужное поле
        employee = Employee.objects.create(position=position, **validated_data)
        return employee

    def update(self, instance, validated_data):
        # Обновление данных сотрудника
        position = validated_data.pop('position_id', None)
        # Обновляем поля сотрудника
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Обновляем позицию сотрудника
        if position is not None:
            instance.position = position
        instance.save()
        return instance

    
    def get_order_count(self, obj):
        # Подсчитываем количество заявок у этого сотрудника
        return Order.objects.filter(employee=obj, status='completed').count()

# --- PositionEmployee ---
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
        # Получаем ID позиции и удаляем его из словаря
        employee = validated_data.pop('employee_id', None)
        position = validated_data.pop('position_id')
        # Создаем сотрудника, передавая ID позиции в нужное поле
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
        """ Валидация данных заказа """
        if data.get('completion_date') and data.get('order_date'):
            if data['completion_date'] < data['order_date']:
                raise serializers.ValidationError("Дата завершения заказа не может быть раньше даты создания.")
        
        if data.get('quantity') and data['quantity'] <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0.")
        
        return data

    def create(self, validated_data):
        # Извлекаем данные о client, service и employee по их ID
        client = validated_data.pop('client_id')
        service = validated_data.pop('service_id')
        employee = validated_data.pop('employee_id')
        # Извлекаем остальные параметры заказа вручную
        order_date = validated_data.get('order_date')
        completion_date = validated_data.get('completion_date')
        quantity = validated_data.get('quantity')
        total_cost = validated_data.get('total_cost')
        status = validated_data.get('status')

        # Создаем заказ с правильными связями
        order = Order.objects.create(
            client=client,
            service=service,
            employee=employee,
            order_date=order_date,
            completion_date=completion_date,
            quantity=quantity,
            total_cost=total_cost,
            status=status
            # **validated_data  # все остальные данные, включая order_date, completion_date и т.д.
        )
        return order

    def update(self, instance, validated_data):
        # Запрещаем изменение client, service и employee
        if 'client_id' in validated_data:
            raise serializers.ValidationError("Client cannot be changed.")
        # if 'service_id' in validated_data:
        #     raise serializers.ValidationError("Service cannot be changed.")
        # if 'employee_id' in validated_data:
        #     raise serializers.ValidationError("Employee cannot be changed.")

        # Обновляем заказ для остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



# --- PaymentOrder ---
class PaymentOrderSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    # order_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Order.objects.all(), write_only=True
    # )

    class Meta:
        model = PaymentOrder
        fields = '__all__'