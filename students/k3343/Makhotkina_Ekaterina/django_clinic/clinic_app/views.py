from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class MedicalCardListCreateView(generics.ListCreateAPIView):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer


class MedicalCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalCard.objects.all()
    serializer_class = MedicalCardSerializer


class DiagnosisListCreateView(generics.ListCreateAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class DiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDiagnosisListCreateView(generics.ListCreateAPIView):
    queryset = AppointmentDiagnosis.objects.all()
    serializer_class = AppointmentDiagnosisSerializer


class AppointmentDiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppointmentDiagnosis.objects.all()
    serializer_class = AppointmentDiagnosisSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class EmployeeScheduleListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeSchedule.objects.all()
    serializer_class = EmployeeScheduleSerializer


class EmployeeScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeSchedule.objects.all()
    serializer_class = EmployeeScheduleSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServicePriceListCreateView(generics.ListCreateAPIView):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer


class ServicePriceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer


class ProvidedServiceListCreateView(generics.ListCreateAPIView):
    queryset = ProvidedService.objects.all()
    serializer_class = ProvidedServiceSerializer


class ProvidedServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProvidedService.objects.all()
    serializer_class = ProvidedServiceSerializer


class PaymentForProvidedServiceListCreateView(generics.ListCreateAPIView):
    queryset = PaymentForProvidedService.objects.all()
    serializer_class = PaymentForProvidedServiceSerializer


class PaymentForProvidedServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentForProvidedService.objects.all()
    serializer_class = PaymentForProvidedServiceSerializer


class AppointmentsByDoctorAPIView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor = Employee.objects.get(id=doctor_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Врач не найден'}, status=status.HTTP_404_NOT_FOUND)

        appointments = Appointment.objects.filter(employee=doctor)
        patient_data = []

        for appointment in appointments:
            patient = appointment.medical_card.patient
            services = ProvidedService.objects.filter(appointment=appointment)

            total_price = 0
            for service in services:
                service_price = ServicePrice.objects.filter(
                    service=service.service,
                    start_date__lte=appointment.appointment_datetime
                )
                if service_price.exists():
                    total_price += service_price.last().price

            patient_data.append({
                'patient_name': f"{patient.last_name} {patient.first_name}",
                'appointment_date': appointment.appointment_datetime,
                'total_cost': total_price
            })

        patient_data.sort(key=lambda x: x['patient_name'])
        return Response({'appointments': patient_data}, status=status.HTTP_200_OK)


class PhonesOfRheumatologistPatientsAPIView(APIView):
    def get(self, request):
        rheumatologist_specialization = "Ревматолог"
        rheumatologists = Employee.objects.filter(specialization=rheumatologist_specialization)
        phone_numbers = set()

        for doctor in rheumatologists:
            appointments = Appointment.objects.filter(employee=doctor)
            for appointment in appointments:
                patient = appointment.medical_card.patient
                if patient.birth_date.year > 1987:
                    phone_numbers.add(patient.phone)

        return Response({'phone_numbers': list(phone_numbers)}, status=status.HTTP_200_OK)


class DoctorsWithWorkDayAPIView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee_schedules = EmployeeSchedule.objects.filter(date=date, is_working_day=True)
            employees = Employee.objects.filter(id__in=[schedule.employee.id for schedule in employee_schedules])
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentsCountByDateAPIView(APIView):
    def get(self, request):
        date_of_appointment = self.request.query_params.get('date')
        if not date_of_appointment:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)
        appointments_count = Appointment.objects.filter(appointment_datetime__date=date_of_appointment).count()

        return Response({"date": date_of_appointment, "appointments_count": appointments_count}, status=status.HTTP_200_OK)


class TotalTreatmentCostByDayAndDoctorAPIView(APIView):
    def get(self, request):
        date = self.request.query_params.get('date')
        if not date:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)

        appointments = Appointment.objects.filter(appointment_datetime__date=date)
        treatment_cost_data = []

        for appointment in appointments:
            provided_services = ProvidedService.objects.filter(appointment=appointment)
            total_cost = 0
            for service in provided_services:
                service_price = ServicePrice.objects.filter(
                    service=service.service,
                    start_date__lte=appointment.appointment_datetime
                ).last()

                if service_price:
                    total_cost += service_price.price * service.quantity
            treatment_cost_data.append({
                'doctor': f"{appointment.employee.last_name} {appointment.employee.first_name}",
                'date': appointment.appointment_datetime.date(),
                'total_cost': total_cost
            })

        result = {}
        for data in treatment_cost_data:
            key = (data['doctor'], data['date'])
            if key not in result:
                result[key] = 0
            result[key] += data['total_cost']

        grouped_result = [
            {
                'doctor': key[0],
                'date': key[1],
                'total_cost': result[key]
            }
            for key in result
        ]

        return Response(grouped_result, status=status.HTTP_200_OK)


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
