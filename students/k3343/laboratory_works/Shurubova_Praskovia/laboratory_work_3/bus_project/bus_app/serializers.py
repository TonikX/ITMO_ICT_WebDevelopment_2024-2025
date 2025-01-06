from rest_framework import serializers
from .models import Driver, Route, Bus, DriverSchedule, BusAssignment, Maintenance


class DriverSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(),
        many=True
    )

    class Meta:
        model = Driver
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class DriverScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSchedule
        fields = "__all__"


class BusAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusAssignment
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = '__all__'
