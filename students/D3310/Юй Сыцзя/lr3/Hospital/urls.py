from rest_framework.routers import DefaultRouter
from django.urls import path, include
from Hospital import views
from Hospital.views import AppointmentsByDoctorAPIView, OtolaryngologistPatientsApiView, DoctorsWithWorkDayAPIView, \
    AppointmentsCountByDateAPIView, TotalTreatmentCostByDayAndDoctorAPIView, PaidPatientsAPIView

router = DefaultRouter()


router.register('patients', views.PatientListView)
router.register('payments', views.PatientPaymentView)
router.register('doctors', views.DoctorViewSet)
router.register('appointments', views.AppointmentListView)
router.register('medical-cards', views.MedicalCardListView)
router.register('doctor-schedules', views.DoctorScheduleView)
router.register('cabinets', views.CabinetListView)
router.register('employment-periods', views.EmploymentPeriodViewSet)
router.register('services', views.ServiceViewSet)
router.register('doctor-patients', views.DoctorPatientViewSet)
router.register('doctor-cabinets', views.DoctorCabinetViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('doctors/<int:doctor_id>/appointments/', AppointmentsByDoctorAPIView.as_view(), name="doctor-appointments"),
    path('otolaryngologist-patients/', OtolaryngologistPatientsApiView.as_view(), name="otolaryngologist"),
    path('doctors-workday/', DoctorsWithWorkDayAPIView.as_view(), name="doctors-with-workday"),
    path('count-by-date/', AppointmentsCountByDateAPIView.as_view(), name="appointments"),
    path('total-cost-by-day/', TotalTreatmentCostByDayAndDoctorAPIView.as_view(), name='total-treatment-cost-by-day-and-doctor'),
    path('paid-patients/', PaidPatientsAPIView.as_view(), name='paid-patients'),
]

