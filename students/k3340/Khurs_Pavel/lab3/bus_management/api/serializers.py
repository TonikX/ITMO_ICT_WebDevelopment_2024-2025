from rest_framework import serializers
from .models import BusType, Bus, Driver, Route, WorkShift

class BusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    bus_type = BusTypeSerializer(read_only=True)                  # Nested read
    bus_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BusType.objects.all(),
        source='bus_type',
        write_only=True
    )

    class Meta:
        model = Bus
        fields = [
            'id', 'registration_number', 'in_service',
            'bus_type', 'bus_type_id'
        ]

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class WorkShiftSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    bus = BusSerializer(read_only=True)
    route = RouteSerializer(read_only=True)

    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        source='driver',
        write_only=True
    )
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(),
        source='bus',
        write_only=True
    )
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(),
        source='route',
        write_only=True
    )

    class Meta:
        model = WorkShift
        fields = '__all__'