from datetime import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(read_only=True)
    arrival_airport = AirportSerializer(read_only=True)
    airline = AirlineSerializer(read_only=True)
    class Meta:
        model = Route
        fields = '__all__'

class TransitSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    departure_airport = AirportSerializer(read_only=True)
    arrival_airport = AirportSerializer(read_only=True)

    class Meta:
        model = Transit
        fields = '__all__'
    
    def create(self, validated_data):
        transit = Transit.objects.create(**validated_data)
        return transit

class AirplaneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneModel
        fields = '__all__'

class AirplaneSerializer(serializers.ModelSerializer):
    airplane_model = AirplaneModelSerializer(read_only=True)
    airline = AirlineSerializer(read_only=True)
    class Meta:
        model = Airplane
        fields = '__all__'

class AirplaneMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneMaintenance
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    airline = AirlineSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create_user(**user_data)
        airline = Airline.objects.get(id=self.context['request'].data['airline'])
        employee = Employee.objects.create(
            user=user,
            airline=airline,
            **validated_data
        )
        return employee

    def update(self, instance, validated_data):
        # Handle password update separately for security
        if 'user' in validated_data and 'password' in validated_data['user']:
            user = instance.user
            user.set_password(validated_data['user']['password'])
            user.is_active = validated_data['user']['is_active']
            user.save()

        user_data = validated_data.pop('user', {})
        # Update user fields
        for attr, value in user_data.items():
            if attr != 'password':
                setattr(instance.user, attr, value)
        instance.user.save()
        
        # Update employee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CrewMemberSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = CrewMember
        fields = '__all__'

class CrewSerializer(serializers.ModelSerializer):
    members = CrewMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = '__all__'

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        crew = Crew.objects.create(**validated_data)

        for member_data in members_data:
            employee_id = member_data.get('employee')
            role = member_data.get('role')
            employee = Employee.objects.get(pk=employee_id)
            CrewMember.objects.create(crew=crew, employee=employee, role=role)

        return crew

class FlightSerializer(serializers.ModelSerializer):
    airplane = AirplaneSerializer()
    crew = CrewSerializer()
    route = RouteSerializer()
    
    class Meta:
        model = Flight
        fields = ['id', 'airplane', 'crew', 'route', 'sold_tickets', 'flight_number', 'flight_status']

    def create(self, validated_data):
        # Extract the full objects from validated_data
        airplane_data = validated_data.pop('airplane')
        crew_data = validated_data.pop('crew')
        route_data = validated_data.pop('route')
        airplane = Airplane.objects.get(id=self.context['request'].data['airplane']['id'])
        crew = Crew.objects.get(id=self.context['request'].data['crew']['id'])
        route = Route.objects.get(id=self.context['request'].data['route']['id'])
        # Create flight with direct references to existing objects
        flight = Flight.objects.create(
            airplane=airplane,        
            crew=crew,
            route=route,
            **validated_data
        )
        
        return flight


