from rest_framework import serializers

from Hospital.models import Patient, Doctor, Appointment, Payment, MedicalCard, DoctorSchedule, Cabinet


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'birth_date']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'appointment_date', 'appointment_time', 'patient', 'doctor', 'cabinet', 'service']


class PaymentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['patient', 'service', 'amount', 'payment_date', 'is_paid']


class MedicalCardSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = MedicalCard
        fields = ['patient', 'record_date', 'diagnosis']


class DoctorSheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'work_date', 'start_time', "is_working"]


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = '__all__'