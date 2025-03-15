from conference_api.serializers import ConferenceSerializer
from rest_framework import serializers

from .models import Contract, Employee, Position, WorkSchedule


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        employee = Employee(**validated_data)
        employee.save()
        return Employee(**validated_data)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class ContractDetailedSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    position = PositionSerializer()

    class Meta:
        model = Contract
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        depth = 0


class ContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ['end_date']

    def create(self, validated_data):
        contract = Contract(**validated_data)
        contract.save()
        return Contract(**validated_data)


class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['end_date', 'working_status']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        depth = 0


class ScheduleDetailedSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()
    conference = ConferenceSerializer()
    class Meta:
        model = WorkSchedule
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        exclude = ['is_done']

    def create(self, validated_data):
        schedule = WorkSchedule(**validated_data)
        schedule.save()
        return WorkSchedule(**validated_data)


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = ['is_done']
