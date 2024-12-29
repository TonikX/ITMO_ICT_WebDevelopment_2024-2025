from rest_framework import serializers
from .models import Airline, AircraftType, Airplane, Route, Flight, TransitStop, Employee, Crew, CrewEmployee, FlightInstance


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'address', 'phone', 'country', 'city', 'info']


class AircraftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftType
        fields = ['id', 'model', 'seats', 'speed']


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ['id', 'number', 'type', 'airline', 'seats', 'speed']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'departure_airport', 'destination_airport', 'distance']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'route', 'airplane', 'departure_time', 'arrival_time', 'sold_tickets']


class TransitStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitStop
        fields = ['id', 'flight', 'stop_airport', 'arrival_time', 'departure_time']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'airline', 'full_name', 'age', 'education', 'experience', 'passport', 'is_active']


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ['id', 'navigator', 'second_pilot']


class CrewEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewEmployee
        fields = ['id', 'crew', 'employee', 'role']


class FlightInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightInstance
        fields = [
            'id',
            'flight',
            'departure_time',
            'arrival_time',
            'actual_departure_time',
            'actual_arrival_time',
            'status',
            'seats_sold'
        ]