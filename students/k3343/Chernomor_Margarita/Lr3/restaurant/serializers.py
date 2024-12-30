from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from restaurant.models import Restaurant, Reservation, Table, Review
from restaurant.utils import time_from_index



class TruncatedTextField(serializers.CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        return value[:97] + '...' if value else value


class TableListSerializer(Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.table_number,
            "description": f'Table for {instance.n_people} people'
        }


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RestaurantListSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address']


class RestaurantDetailSerializer(ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    tables = TableListSerializer(read_only=True, many=True, source='table_set')

    class Meta:
        model = Restaurant
        fields = '__all__'


class ReservationSerializer(ModelSerializer):
    time_start = serializers.SerializerMethodField()
    time_end = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['time_start', 'time_end']

    def get_time_start(self, obj):
        return time_from_index(obj.time_start)

    def get_time_end(self, obj):
        return time_from_index(obj.time_end)


class TableWithReservationSerializer(ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True, source='reservation_set')

    class Meta:
        model = Table
        fields = ['id', 'table_number', 'reservations', 'n_people']


class ReservationCreateSerializer(ModelSerializer):
    comment = serializers.CharField(required=False)

    class Meta:
        model = Reservation
        fields = [
            'dt_reservation',
            'time_start',
            'time_end',
            'n_people',
            'comment'
        ]


class ReviewSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    comment = TruncatedTextField()

    class Meta:
        model = Review
        fields = ['user', 'dt_created', 'rating', 'comment']
