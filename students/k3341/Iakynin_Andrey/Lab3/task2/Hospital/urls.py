from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientListView, DoctorListView, AppointmentListView, PatientPaymentView, MedicalCardListView, \
    DoctorScheduleView, CabinetListView

router = DefaultRouter()
router.register('patients', PatientListView)
router.register('doctors', DoctorListView)
router.register('appointments', AppointmentListView)
router.register('payments', PatientPaymentView)
router.register('medical_cards', MedicalCardListView)
router.register("doctor_schedule", DoctorScheduleView )
router.register('cabinets', CabinetListView)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]