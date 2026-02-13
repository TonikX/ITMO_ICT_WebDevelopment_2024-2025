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
    client = ClientSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    client_passport = serializers.CharField(write_only=True, source='client.passport')
    room_number = serializers.IntegerField(write_only=True, source='room.number')

    class Meta:
        model = Stay
        fields = ['id', 'client', 'room', 'check_in', 'check_out',
                  'client_passport', 'room_number']

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        room_data = validated_data.pop('room')
        client, _ = Client.objects.get_or_create(passport=client_data['passport'], defaults=client_data)
        room = Room.objects.get(number=room_data['number'])
        validated_data['client'] = client
        validated_data['room'] = room
        return super().create(validated_data)


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'
