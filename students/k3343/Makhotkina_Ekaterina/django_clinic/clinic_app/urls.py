from django.urls import path
from .views import *


app_name = "clinic_app"

urlpatterns = [
    path('patients/', PatientListCreateView.as_view()),
    path('patients/<int:pk>/', PatientDetailView.as_view()),
    path('medical_cards/', MedicalCardListCreateView.as_view()),
    path('medical_cards/<int:pk>/', MedicalCardDetailView.as_view()),
    path('employees/', EmployeeListCreateView.as_view()),
    path('employees/<int:pk>/', EmployeeDetailView.as_view()),
    path('diagnosis/', DiagnosisListCreateView.as_view()),
    path('diagnosis/<int:pk>/', DiagnosisDetailView.as_view()),
    path('appointments/', AppointmentListCreateView.as_view()),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view()),
    path('appointment_diagnosis/', AppointmentDiagnosisListCreateView.as_view()),
    path('appointment_diagnosis/<int:pk>/', AppointmentDiagnosisDetailView.as_view()),
    path('services/', ServiceListCreateView.as_view()),
    path('services/<int:pk>/', ServiceDetailView.as_view()),
    path('service_prices/', ServicePriceListCreateView.as_view()),
    path('service_prices/<int:pk>/', ServicePriceDetailView.as_view()),
    path('provided_services/', ProvidedServiceListCreateView.as_view()),
    path('provided_services/<int:pk>/', ProvidedServiceDetailView.as_view()),
    path('payments/', PaymentForProvidedServiceListCreateView.as_view()),
    path('payments/<int:pk>/', PaymentForProvidedServiceDetailView.as_view()),
    path('appointments_by_doctor/<int:doctor_id>/', AppointmentsByDoctorAPIView.as_view()),
    path('phones_of_revmalogist_patients/', PhonesOfRheumatologistPatientsAPIView.as_view()),
    path('paid_patients/', PaidPatientsAPIView.as_view()),
    path('rooms/', RoomListCreateView.as_view()),
    path('rooms/<int:pk>/', RoomDetailView.as_view()),
    path('employee-schedules/', EmployeeScheduleListCreateView.as_view()),
    path('employee-schedules/<int:pk>/', EmployeeScheduleDetailView.as_view()),
    path('doctors-with-work-day/', DoctorsWithWorkDayAPIView.as_view()),
    path('appointments-count-by-date/', AppointmentsCountByDateAPIView.as_view()),
    path('total-treatment-cost-by-day-and-doctor/', TotalTreatmentCostByDayAndDoctorAPIView.as_view()),
]
