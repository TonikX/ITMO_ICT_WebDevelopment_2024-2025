from rest_framework import serializers
from .models import BusType, Bus, Driver, Route, WorkShift


class BusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    bus_type = BusTypeSerializer()

    class Meta:
        model = Bus
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'id', 'number',
            'start_point',
            'end_point',
            'operation_start_time',
            'operation_end_time',
            'interval',
            'duration'
        ]


class WorkShiftSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    bus = BusSerializer()
    route = RouteSerializer()

    class Meta:
        model = WorkShift
        fields = ['id', 'date', 'shift_start_time', 'shift_end_time', 'status', 'reason', 'driver', 'bus', 'route']

    def validate(self, data):
        # Пример валидации перекрывающихся смен
        driver_id = data.get('driver').get('id')  # Получаем ID водителя из вложенного объекта
        date = data.get('date')

        overlapping_shifts = WorkShift.objects.filter(
            driver_id=driver_id,
            date=date
        )

        if overlapping_shifts.exists():
            raise serializers.ValidationError("Driver already has a shift on this date.")

        return data

    def create(self, validated_data):
        driver_data = validated_data.pop('driver')
        bus_data = validated_data.pop('bus')
        route_data = validated_data.pop('route')

        driver = Driver.objects.create(**driver_data)
        bus = Bus.objects.create(**bus_data)
        route = Route.objects.create(**route_data)

        work_shift = WorkShift.objects.create(driver=driver, bus=bus, route=route, **validated_data)

        return work_shift

class RouteTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

