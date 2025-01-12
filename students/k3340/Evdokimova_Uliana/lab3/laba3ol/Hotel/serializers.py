from rest_framework import serializers
from .models import UserAccount, Room, RoomType, RoomTypePrice, Employee, Position, SalaryHistory, Contract, WorkSchedule, Booking


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'firstname', 'lastname', 'patronymic', 'phone', 'date_joined', 'birth_date', 'is_staff', 'is_active', 'groups', 'user_permissions']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'places', 'description']


class RoomTypePriceSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer()

    class Meta:
        model = RoomTypePrice
        fields = ['id', 'day_price', 'start_date', 'end_date', 'room_type']


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = ['id', 'number', 'area', 'is_occupied', 'is_cleaned', 'floor', 'room_type']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'firstname', 'lastname', 'patronymic', 'email', 'phone']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'description']


class SalaryHistorySerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = SalaryHistory
        fields = ['id', 'salary', 'start_date', 'end_date', 'position']


class ContractSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    position = PositionSerializer()

    class Meta:
        model = Contract
        fields = ['id', 'start_date', 'end_date', 'working_status', 'employee', 'position']


class WorkScheduleSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()
    room = RoomSerializer()

    class Meta:
        model = WorkSchedule
        fields = ['id', 'start_time', 'end_time', 'is_done', 'contract', 'room']


class BookingSerializer(serializers.ModelSerializer):
    client = UserAccountSerializer()
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'booking_date', 'from_town', 'check_in_time', 'departure_time', 'full_days', 'state', 'payment_status', 'client', 'room']
