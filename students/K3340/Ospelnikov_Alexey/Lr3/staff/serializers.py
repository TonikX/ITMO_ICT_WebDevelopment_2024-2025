from rest_framework import serializers
from .models import Employee, RoomClean


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class RoomCleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomClean
        fields = '__all__'