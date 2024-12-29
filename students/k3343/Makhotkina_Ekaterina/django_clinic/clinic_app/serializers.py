from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class MedicalCardSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = MedicalCard
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDiagnosis
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


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


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    room = RoomSerializer()

    class Meta:
        model = EmployeeSchedule
        fields = '__all__'
