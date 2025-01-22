from rest_framework import serializers
from clinic.models import (
    Patient, MedicalCard, Diagnosis, Appointment, AppointmentDiagnosis,
    Employee, EmployeeSchedule, Room, EmploymentPeriod, Position,
    Specialization, EmployeeSpecialization, Service, ServicePrice,
    ProvidedService, PaymentForProvidedService
)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class MedicalCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCard
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    medical_card = MedicalCardSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDiagnosis
        fields = '__all__'


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number')
    internal_phone = serializers.CharField(source='room.internal_phone')

    class Meta:
        model = EmployeeSchedule
        fields = ['date', 'is_working_day', 'room_number', 'internal_phone']


class EmployeeSerializer(serializers.ModelSerializer):
    schedules = EmployeeScheduleSerializer(many=True)  # Добавляем информацию о сменах

    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'specialization', 'schedules', 'education', 'gender', 'birth_date']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class EmploymentPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentPeriod
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class EmployeeSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSpecialization
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServicePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrice
        fields = '__all__'


class ProvidedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvidedService
        fields = '__all__'


class PaymentForProvidedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentForProvidedService
        fields = '__all__'

