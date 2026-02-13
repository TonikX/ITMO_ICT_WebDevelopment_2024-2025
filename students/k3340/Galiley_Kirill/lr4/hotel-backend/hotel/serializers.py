from rest_framework import serializers
from .models import *


class RoomSerializer(serializers.ModelSerializer):
    is_free = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class StaySerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source='client',
        write_only=True
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True
    )

    client = ClientSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Stay
        fields = ['id', 'client', 'client_id', 'room', 'room_id', 'check_in', 'check_out']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['client_name'] = f"{instance.client.last_name} {instance.client.first_name}"

        data['room_number'] = instance.room.number

        data['client_full'] = data.pop('client')
        data['room_full'] = data.pop('room')

        return data

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'
