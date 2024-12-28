from rest_framework import serializers
from .models import Room, RoomType


class RoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['is_cleaned', 'is_occupied']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomDetailedSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer()
    class Meta:
        model = Room
        fields = '__all__'
