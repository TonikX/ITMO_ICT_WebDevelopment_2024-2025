from rest_framework import serializers
from .models import Client, RoomType, Room, RoomPrice, Booking, JobTitle, Employee, EmploymentContract, CleaningSchedule
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class RoomPriceSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)

    class Meta:
        model = RoomPrice
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmploymentContractSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    job_title = JobTitleSerializer(read_only=True)

    class Meta:
        model = EmploymentContract
        fields = '__all__'


class CleaningScheduleSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    cleaner = EmployeeSerializer(read_only=True)

    class Meta:
        model = CleaningSchedule
        fields = '__all__'