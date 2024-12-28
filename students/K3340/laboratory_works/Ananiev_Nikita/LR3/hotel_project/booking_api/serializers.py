from rest_framework import serializers
from .models import Booking
from hotel_api.serializers import RoomSerializer
from auth_api.serializers import CustomUserSerializer


class BookingDetailedSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer()
    room = RoomSerializer()
    class Meta:
        model = Booking
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['client', 'room', 'booking_date', 'from_town']

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.payment_status = 'not paid'
        booking.state = 'booked'
        booking.save()
        return Booking(**validated_data)


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in_time', 'departure_time', 'full_days', 'state', 'payment_status']
        depth = 1
