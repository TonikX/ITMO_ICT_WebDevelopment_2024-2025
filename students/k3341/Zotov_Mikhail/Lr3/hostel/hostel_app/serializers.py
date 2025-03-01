from rest_framework import serializers

from .models import *


class FloorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorSchedule
        fields = ['floor', 'day_of_week']


class CleaningAssignmentSerializer(serializers.ModelSerializer):
    floor_schedule = FloorScheduleSerializer()

    class Meta:
        model = CleaningAssignment
        fields = ['floor_schedule']

    def create(self, validated_data):
        floor_schedule_data = validated_data.pop('floor_schedule')
        floor_schedule, _ = FloorSchedule.objects.get_or_create(**floor_schedule_data)
        return CleaningAssignment.objects.create(floor_schedule=floor_schedule, **validated_data)

    def update(self, instance, validated_data):
        floor_schedule_data = validated_data.pop('floor_schedule', None)
        if floor_schedule_data:
            floor_schedule, _ = FloorSchedule.objects.get_or_create(**floor_schedule_data)
            instance.floor_schedule = floor_schedule
        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    cleaning_assignments = CleaningAssignmentSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'cleaning_assignments']

    def create(self, validated_data):
        cleaning_assignments_data = validated_data.pop('cleaning_assignments')
        employee = Employee.objects.create(**validated_data)
        for assignment_data in cleaning_assignments_data:
            CleaningAssignmentSerializer().create({**assignment_data, 'employee': employee})
        return employee

    def update(self, instance, validated_data):
        cleaning_assignments_data = validated_data.pop('cleaning_assignments', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if cleaning_assignments_data is not None:
            instance.cleaning_assignments.all().delete()
            for assignment_data in cleaning_assignments_data:
                CleaningAssignmentSerializer().create({**assignment_data, 'employee': instance})
        return instance


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    floor = FloorSerializer()

    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'passport_number': {'validators': []},
        }


class ClientRoomSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    room_number = serializers.SerializerMethodField()

    class Meta:
        model = ClientRoom
        fields = ['id', 'client', 'room', 'room_number', 'check_in_date', 'check_out_date', 'count_of_clients']

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        passport_number = client_data.get('passport_number')
        client, created = Client.objects.get_or_create(
            passport_number=passport_number,
            defaults=client_data
        )
        client_room = ClientRoom.objects.create(client=client, **validated_data)
        return client_room

    def update(self, instance, validated_data):
        client_data = validated_data.pop('client', None)
        if client_data:
            for attr, value in client_data.items():
                setattr(instance.client, attr, value)
            instance.client.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def get_room_number(cls, obj):
        return obj.room.number if obj.room else None
