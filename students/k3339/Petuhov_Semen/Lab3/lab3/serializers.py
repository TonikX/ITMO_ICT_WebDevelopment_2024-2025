from rest_framework import serializers
from .models import Client, Ticket, Flight, Crew, Aircraft, Schedule, Airport, TransitStop

# Serializer для Клиента и Билетов
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(source='ticket_set', many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['passenger_data', 'full_name', 'phone_number', 'tickets']

# Serializer для Экипажа
class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'

# Serializer для Самолета
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

# Serializer для Рейса
class FlightSerializer(serializers.ModelSerializer):
    crew = CrewSerializer(source='crew_set', many=True, read_only=True)
    aircraft = AircraftSerializer(source='onBoard_number', read_only=True)
    schedule = serializers.StringRelatedField(source='schedule_number')

    class Meta:
        model = Flight
        fields = ['flight_number', 'departure_date', 'arrival_date', 'status', 'aircraft', 'crew', 'schedule']

# Serializer для Расписания, Аэропорта и Транзитных посадок
class TransitStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitStop
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    airport = AirportSerializer(source='airport_number', read_only=True)
    transit_stops = TransitStopSerializer(source='transitstop_set', many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ['schedule_number', 'departure_time', 'arrival_time', 'airport', 'transit_stops']