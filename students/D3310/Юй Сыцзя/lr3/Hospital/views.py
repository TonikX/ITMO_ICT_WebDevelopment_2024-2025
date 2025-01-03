from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from Hospital import models
from Hospital.models import Patient, Doctor, Payment, Appointment, MedicalCard, Cabinet, DoctorSchedule, \
    EmploymentPeriod, Service, DoctorPatient, DoctorCabinet, ServicePayment
from Hospital.serializers import PatientSerializer, PaymentSerializer, DoctorSerializer, AppointmentSerializer, \
    MedicalCardSerializer, DoctorScheduleSerializer, CabinetSerializer, EmploymentPeriodSerializer, ServiceSerializer, \
    DoctorPatientSerializer, DoctorCabinetSerializer


class PatientListView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientPaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class AppointmentListView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class MedicalCardListView(viewsets.ModelViewSet):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer


class DoctorScheduleView(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer


class CabinetListView(viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer


class EmploymentPeriodViewSet(viewsets.ModelViewSet):
    queryset = EmploymentPeriod.objects.all()
    serializer_class = EmploymentPeriodSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class DoctorPatientViewSet(viewsets.ModelViewSet):
    queryset = DoctorPatient.objects.all()
    serializer_class = DoctorPatientSerializer


class DoctorCabinetViewSet(viewsets.ModelViewSet):
    queryset = DoctorCabinet.objects.all()
    serializer_class = DoctorCabinetSerializer


class AppointmentsByDoctorAPIView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': "Врач не найден"}, status=status.HTTP_404_NOT_FOUND)

        appointments = (
            Appointment.objects.filter(doctor=doctor)
            .select_related('patient', 'service')
            .order_by('patient__last_name', 'patient__first_name')
        )

        result = []
        for appointment in appointments:
            service_payment = ServicePayment.objects.filter(service=appointment.service).first()
            price = service_payment.amount if service_payment else 0.00

            result.append({
                'patient': f"{appointment.patient.last_name} {appointment.patient.first_name}",
                'appointment_date': appointment.appointment_date,
                'appointment_time': appointment.appointment_time,
                'service': appointment.service.service_name,
                'price': price
            })

        return Response({
            'doctor': f"{doctor.last_name} {doctor.first_name}",
            'appointments': result
        }, status=status.HTTP_200_OK)


class OtolaryngologistPatientsApiView(APIView):
    def get(self, request):
        otolaryngologists = Doctor.objects.filter(speciality='Отоларинголог')
        appointments = Appointment.objects.filter(doctor__in=otolaryngologists)
        patients = Patient.objects.filter(id__in=appointments.values_list('patient_id', flat=True),
                                          birth_date__year__gte=1987).values('first_name','last_name','phone_number')

        return JsonResponse(list(patients), safe=False)


class DoctorsWithWorkDayAPIView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedules = DoctorSchedule.objects.filter(work_date=date, is_working=True)

            serializer = DoctorScheduleSerializer(schedules, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentsCountByDateAPIView(APIView):
    def get(self, request):
        date_str = self.request.query_params.get('date')
        if not date_str:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        appointments_count = Appointment.objects.filter(appointment_date=date).count()
        return Response({"date": date, "appointments_count": appointments_count}, status=status.HTTP_200_OK)


class TotalTreatmentCostByDayAndDoctorAPIView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        appointments = Appointment.objects.filter(appointment_date=date)

        treatment_cost = (
            appointments
            .values('doctor')
            .annotate(total_cost=Sum('service__service_payments__amount'))
            .order_by('doctor')
        )

        result = []
        for entry in treatment_cost:
            doctor = Doctor.objects.get(id=entry['doctor'])
            result.append({
                'doctor': f"{doctor.first_name} {doctor.last_name}",
                'date': date,
                'total_cost': entry['total_cost'] or 0
            })

        return Response(result, status=status.HTTP_200_OK)


class PaidPatientsAPIView(APIView):
    def get(self, request):
        paid_patients = Payment.objects.filter(is_paid=True).values('patient').distinct()

        patients_data = []
        for payment in paid_patients:
            patient_id = payment['patient']
            patient_objs = Payment.objects.filter(patient_id=patient_id)

            for patient_obj in patient_objs:
                patients_data.append({
                    "first_name": patient_obj.patient.first_name,
                    "last_name": patient_obj.patient.last_name,
                    "middle_name": patient_obj.patient.middle_name,
                    "address": patient_obj.patient.address,
                    "phone_number": patient_obj.patient.phone_number,
                    "birth_date": patient_obj.patient.birth_date,
                })

        return Response(patients_data, status=status.HTTP_200_OK)