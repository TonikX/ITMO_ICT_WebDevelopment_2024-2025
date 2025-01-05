from rest_framework import serializers
from .models import Room, Client, Staff, CleaningSchedule, Reservation, Report
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import User

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class CleaningScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.__str__', read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'
        extra_fields = ['staff_name']

class ReservationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    room_number = serializers.IntegerField(source='room.number', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        extra_fields = ['client_name', 'room_number']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'is_admin']  # Админ-роль недоступна при регистрации

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'is_admin']