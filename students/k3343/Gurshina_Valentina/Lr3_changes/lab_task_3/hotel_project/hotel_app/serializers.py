from djoser.views import User
from rest_framework import serializers

from hotel_app.models import Room, Client, Reservation, Employee, EmployeeSchedule


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class NestedReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    admin = SuperUserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = EmployeeSchedule
        fields = '__all__'

class ReservationCreateWithAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class EmployeeScheduleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeSchedule
        fields = ['employee_id', 'day_of_week', 'floor']


class EmployeeScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSchedule
        fields = '__all__'

