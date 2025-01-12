from rest_framework import serializers
from .models import BusDriver, Bus, Route, WorkSchedule


class BusDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusDriver
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class WorkScheduleSerializer(serializers.ModelSerializer):
    driver = BusDriverSerializer()
    bus = BusSerializer()
    route = RouteSerializer()
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = WorkSchedule
        fields = '__all__'


class DriverWorkScheduleSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    driver = BusDriverSerializer(read_only=True, many=True)

    class Meta:
        model = WorkSchedule
        fields = "__all__"
