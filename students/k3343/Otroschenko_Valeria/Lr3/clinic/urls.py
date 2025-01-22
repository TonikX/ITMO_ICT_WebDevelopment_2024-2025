from rest_framework import routers
from clinic import views
from django.urls import path, include

from clinic.views import PatientsByDoctorAPIView, PatientsBySpecializationAndBirthYearAPIView, \
     AppointmentsCountByDateAPIView, TreatmentCostByDateAndDoctorAPIView, \
    PaidPatientsAPIView

router = routers.DefaultRouter()

router.register('patient', views.PatientViewSet)
router.register('medicalcard', views.MedicalCardViewSet)
router.register('diagnosis', views.DiagnosisViewSet)
router.register('appointment', views.AppointmentViewSet)
router.register('appointment-diagnosis', views.AppointmentDiagnosisViewSet)
router.register('employee', views.EmployeeViewSet)
router.register('employee-schedule', views.EmployeeScheduleViewSet)
router.register('room', views.RoomViewSet)
router.register('employment-period', views.EmploymentPeriodViewSet)
router.register('position', views.PositionViewSet)
router.register('specialization', views.SpecializationViewSet)
router.register('employee-specialization', views.EmployeeSpecializationViewSet)
router.register('service', views.ServiceViewSet)
router.register('service-price', views.ServicePriceViewSet)
router.register('provided-service', views.ProvidedServiceViewSet)
router.register('payment-for-provided-service', views.PaymentForProvidedServiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('patients-by-doctor/<int:doctor_id>/', PatientsByDoctorAPIView.as_view(), name='patients-by-doctor'),
    path('otolaryngologist-patients/', PatientsBySpecializationAndBirthYearAPIView.as_view(), name='otolaryngologist-patients'),
    path('appointments-count-by-date/', AppointmentsCountByDateAPIView.as_view(), name='appointments-count-by-date'),
    path('treatment-cost-by-date-and-doctor/', TreatmentCostByDateAndDoctorAPIView.as_view(), name='treatment-cost-by-date-and-doctor'),
    path('paid-patients/', PaidPatientsAPIView.as_view(), name='paid-patients')
]
