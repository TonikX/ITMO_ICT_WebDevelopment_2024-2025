from rest_framework import serializers
from .models import (
    RoomType, Room, Guest, Booking, Employee, CleaningAssignment
)

from datetime import date
from django.db.models import Q


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'capacity', 'price_per_day']


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)  # вложенный тип номера
    room_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(),
        source='room_type',
        write_only=True
    )

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'room_type', 'room_type_id', 'phone']


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'passport', 'last_name', 'first_name', 'patronymic', 'city']


class BookingSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=Guest.objects.all(),
        source='guest',
        write_only=True,
        required=True
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True,
        required=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'guest', 'guest_id', 'room', 'room_id', 'check_in', 'check_out']
        read_only_fields = ['id', 'guest', 'room']

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        room = data.get('room')

        if not check_in:
            raise serializers.ValidationError({"check_in": "Обязательное поле"})

        if check_out and check_out <= check_in:
            raise serializers.ValidationError(
                {"check_out": "Дата выезда должна быть позже даты заезда"}
            )

        today = date.today()
        if check_in < today:
            raise serializers.ValidationError(
                {"check_in": "Нельзя заселять на прошедшую дату"}
            )

        # Проверка пересечения с существующими бронированиями
        conflicting = Booking.objects.filter(
            Q(room=room),
            Q(check_in__lte=check_out or date.max),  # до конца новой брони или бесконечно
            Q(check_out__gt=check_in) | Q(check_out__isnull=True)
        ).exclude(id=self.instance.id if self.instance else None)  # исключаем себя при обновлении

        if conflicting.exists():
            raise serializers.ValidationError(
                {"non_field_errors": "Номер уже занят в указанный период"}
            )

        return data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'patronymic', 'is_active']


class CleaningAssignmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = CleaningAssignment
        fields = ['id', 'employee', 'employee_id', 'floor', 'day_of_week', 'day_of_week_display']