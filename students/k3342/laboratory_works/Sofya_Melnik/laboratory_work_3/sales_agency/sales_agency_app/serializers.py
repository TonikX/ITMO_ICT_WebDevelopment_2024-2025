from rest_framework import serializers
from .models import Client, Service, PriceList, Position, Employee, PositionEmployee, Order, PaymentOrder

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PriceListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = PriceList
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'

class PositionEmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = PositionEmployee
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    service = ServiceSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class PaymentOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = PaymentOrder
        fields = '__all__'
