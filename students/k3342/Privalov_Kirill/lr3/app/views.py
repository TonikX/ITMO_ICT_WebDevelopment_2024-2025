from .filters import LaborContractFilter, ScheduleFilter
from rest_framework.viewsets import ModelViewSet
from .models import (
    Patient, MedicalCard, Doctor, Position, LaborContract, Schedule,
    Office, Visit, Diagnosis, VisitDiagnosis, Service, ServicePrice, VisitService, Payment
)
from .serializers import (
    PatientSerializer, MedicalCardSerializer, DoctorSerializer, PositionSerializer, LaborContractSerializer,
    ScheduleSerializer, OfficeSerializer, VisitSerializer, DiagnosisSerializer, VisitDiagnosisSerializer,
    ServiceSerializer, ServicePriceSerializer, VisitServiceSerializer, PaymentSerializer
)
from django_filters.rest_framework import DjangoFilterBackend


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class MedicalCardViewSet(ModelViewSet):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer

class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class LaborContractViewSet(ModelViewSet):
    queryset = LaborContract.objects.all()
    serializer_class = LaborContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LaborContractFilter

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter
class OfficeViewSet(ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class DiagnosisViewSet(ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

class VisitDiagnosisViewSet(ModelViewSet):
    queryset = VisitDiagnosis.objects.all()
    serializer_class = VisitDiagnosisSerializer

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServicePriceViewSet(ModelViewSet):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer

class VisitServiceViewSet(ModelViewSet):
    queryset = VisitService.objects.all()
    serializer_class = VisitServiceSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer