
from rest_framework import serializers

from booking.models import Booking
from rooms.serializers import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingRoomSerializer(serializers.ModelSerializer):
    room_id = RoomSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'prepayment', 'guest_count', 'room_id']