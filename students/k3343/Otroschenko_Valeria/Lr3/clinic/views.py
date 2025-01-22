from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from clinic import models
from clinic.models import (
    Patient, MedicalCard, Diagnosis, Appointment, AppointmentDiagnosis,
    Employee, EmployeeSchedule, Room, EmploymentPeriod, Position,
    Specialization, EmployeeSpecialization, Service, ServicePrice,
    ProvidedService, PaymentForProvidedService
)
from clinic.serializers import (
    PatientSerializer, MedicalCardSerializer, DiagnosisSerializer, AppointmentSerializer,
    AppointmentDiagnosisSerializer, EmployeeSerializer, EmployeeScheduleSerializer,
    RoomSerializer, EmploymentPeriodSerializer, PositionSerializer,
    SpecializationSerializer, EmployeeSpecializationSerializer, ServiceSerializer,
    ServicePriceSerializer, ProvidedServiceSerializer, PaymentForProvidedServiceSerializer
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class MedicalCardViewSet(viewsets.ModelViewSet):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDiagnosisViewSet(viewsets.ModelViewSet):
    queryset = AppointmentDiagnosis.objects.all()
    serializer_class = AppointmentDiagnosisSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeScheduleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSchedule.objects.all()
    serializer_class = EmployeeScheduleSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class EmploymentPeriodViewSet(viewsets.ModelViewSet):
    queryset = EmploymentPeriod.objects.all()
    serializer_class = EmploymentPeriodSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class EmployeeSpecializationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSpecialization.objects.all()
    serializer_class = EmployeeSpecializationSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServicePriceViewSet(viewsets.ModelViewSet):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer


class ProvidedServiceViewSet(viewsets.ModelViewSet):
    queryset = ProvidedService.objects.all()
    serializer_class = ProvidedServiceSerializer


class PaymentForProvidedServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentForProvidedService.objects.all()
    serializer_class = PaymentForProvidedServiceSerializer


class PatientsByDoctorAPIView(APIView):
    def get(self, request, doctor_id):
        appointments = Appointment.objects.filter(employee_id=doctor_id).select_related('patient', 'medical_card')
        appointment_data = []
        for appointment in appointments:
            provided_services = appointment.providedservice_set.all()
            service_prices = ServicePrice.objects.filter(service__in=provided_services.values('service'))
            total_price = sum(service_price.price for service_price in service_prices)
            appointment_data.append({
                'patient_name': f"{appointment.patient.last_name} {appointment.patient.first_name}",
                'appointment_datetime': appointment.appointment_datetime,
                'total_price': total_price
            })
        appointment_data.sort(key=lambda x: x['patient_name'])
        return Response(appointment_data)



class PatientsBySpecializationAndBirthYearAPIView(APIView):
    def get(self, request):
        patients = Patient.objects.filter(
            appointments__employee__employeespecialization__specialization__specialization="Отоларинголог",
            birth_date__year__gt=1987
        ).distinct()
        patient_info = [{
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'phone': patient.phone
        } for patient in patients]

        return Response(patient_info)

class AppointmentsCountByDateAPIView(APIView):
    def get(self, request):
        try:
            appointments_count = Appointment.objects.values('appointment_datetime__date').annotate(count=Count('id')).order_by('appointment_datetime__date')
            return Response(appointments_count)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TreatmentCostByDateAndDoctorAPIView(APIView):
    def get(self, request):
        cost_data = []
        appointments = Appointment.objects.all()

        for appointment in appointments:
            provided_services = ProvidedService.objects.filter(appointment=appointment)

            services = provided_services.values_list('service', flat=True)

            service_prices = ServicePrice.objects.filter(service__in=services)

            total_price = sum(service_price.price for service_price in service_prices)

            cost_data.append({
                'doctor_name': f"{appointment.employee.last_name} {appointment.employee.first_name}",
                'appointment_date': appointment.appointment_datetime.date(),
                'total_cost': total_price
            })

        return Response(cost_data)



class PaidPatientsAPIView(APIView):
    def get(self, request):
        paid_services = PaymentForProvidedService.objects.filter(payment_status="Paid")
        paid_patients = set()
        for paid_service in paid_services:
            appointment = paid_service.provided_service.appointment
            patient = appointment.medical_card.patient
            paid_patients.add(patient)
        data = [
            {
                "last_name": patient.last_name,
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "phone": patient.phone,
            }
            for patient in paid_patients
        ]

        return Response(data, status=status.HTTP_200_OK)