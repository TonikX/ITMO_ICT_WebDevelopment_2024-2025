from rest_framework import serializers
from .models import (
    Patient,
    MedicalCard,
    Doctor,
    EmploymentPeriod,
    DoctorSchedule,
    Cabinet,
    Service,
    Payment,
    Appointment,
    DoctorPatient,
    DoctorCabinet,
)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'address', 'phone_number', 'birth_date']


class MedicalCardSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = MedicalCard
        fields = ['id', 'patient', 'record_date', 'diagnosis']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'sex', 'education', 'birth_date', 'speciality']


class EmploymentPeriodSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = EmploymentPeriod
        fields = ['id', 'doctor', 'start_date', 'end_date']


class DoctorScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'work_date', 'start_time', 'end_time', 'is_working']


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'number']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'description']


class PaymentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'patient', 'service', 'amount', 'payment_date', 'is_paid']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    cabinet = CabinetSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'cabinet', 'service', 'appointment_date', 'appointment_time']


class DoctorPatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()

    class Meta:
        model = DoctorPatient
        fields = ['id', 'doctor', 'patient', 'date_started', 'date_ended']


class DoctorCabinetSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    cabinet = CabinetSerializer()

    class Meta:
        model = DoctorCabinet
        fields = ['id', 'doctor', 'cabinet', 'date_assigned']
