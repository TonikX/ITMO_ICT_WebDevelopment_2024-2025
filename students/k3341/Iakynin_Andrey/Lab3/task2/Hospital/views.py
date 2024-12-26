from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from Hospital.models import Patient, Doctor, Appointment, Payment, MedicalCard, DoctorSchedule, Cabinet
from Hospital.serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, PaymentSerializer, \
    MedicalCardSerializer, DoctorSheduleSerializer, CabinetSerializer


class PatientListView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get(self, request, *args, **kwargs):
        patient_id = kwargs.get('id')
        if patient_id:
            patient = self.get_queryset().filter(id=patient_id).first()
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorListView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self,request,*args,**kwargs):
        doctor_id = kwargs.get('id')
        if doctor_id:
            doctor = self.get_queryset().filter(id=doctor_id).first()
        serializer = self.get_serializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentListView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class PatientPaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class MedicalCardListView(viewsets.ModelViewSet):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer


class DoctorScheduleView(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorSheduleSerializer


class CabinetListView(viewsets.ModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer