from rest_framework import serializers
from .models import (
    Patient, MedicalCard, Doctor, Position, LaborContract, Schedule,
    Office, Visit, Diagnosis, VisitDiagnosis, Service, ServicePrice, VisitService, Payment
)

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)
    positionId = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        write_only=True,
        source='position'
    )
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class MedicalCardSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patientId = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, source='patient'
    )

    class Meta:
        model = MedicalCard
        fields = '__all__'

class LaborContractSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctorId = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True, source='doctor'
    )

    class Meta:
        model = LaborContract
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctorId = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True, source='doctor'
    )

    class Meta:
        model = Schedule
        fields = '__all__'

class OfficeSerializer(serializers.ModelSerializer):
    responsibleDoctor = DoctorSerializer(read_only=True)
    responsibleDoctorId = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True, source='responsible_doctor', allow_null=True
    )

    class Meta:
        model = Office
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class VisitDiagnosisSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(read_only=True)
    visitId = serializers.PrimaryKeyRelatedField(
        queryset=Visit.objects.all(), write_only=True, source='visit'
    )
    diagnosis = DiagnosisSerializer(read_only=True)
    diagnosisId = serializers.PrimaryKeyRelatedField(
        queryset=Diagnosis.objects.all(), write_only=True, source='diagnosis'
    )

    class Meta:
        model = VisitDiagnosis
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patientId = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, source='patient'
    )
    doctor = DoctorSerializer(read_only=True)
    doctorId = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), write_only=True, source='doctor'
    )
    # office = OfficeSerializer(read_only=True)
    # officeId = serializers.PrimaryKeyRelatedField(
    #     queryset=Office.objects.all(), write_only=True, source='office', allow_null=True
    # )
    visitDiagnoses = VisitDiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ServicePriceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    serviceId = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True, source='service'
    )

    class Meta:
        model = ServicePrice
        fields = '__all__'

class VisitServiceSerializer(serializers.ModelSerializer):
    visit = VisitSerializer(read_only=True)
    visitId = serializers.PrimaryKeyRelatedField(
        queryset=Visit.objects.all(), write_only=True, source='visit'
    )
    service = ServiceSerializer(read_only=True)
    serviceId = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True, source='service'
    )

    class Meta:
        model = VisitService
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    visitService = VisitServiceSerializer(read_only=True)
    visitServiceId = serializers.PrimaryKeyRelatedField(
        queryset=VisitService.objects.all(), write_only=True, source='visit_service'
    )

    class Meta:
        model = Payment
        fields = '__all__'