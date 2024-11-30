from sched import scheduler

from rest_framework import serializers
from .models import Bus, Route, Driver, Schedule, Incident

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    bus = BusSerializer()
    route = RouteSerializer()
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class DriverScheduleSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    driver = DriverSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = "__all__"
