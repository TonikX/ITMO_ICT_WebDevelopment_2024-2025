from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, ClientViewSet, CleaningScheduleViewSet, RoomViewSet, ReservationViewSet, ReportViewSet


router = DefaultRouter()
router.register('staff', StaffViewSet)
router.register('clients', ClientViewSet)
router.register('cleaning-schedule', CleaningScheduleViewSet)
router.register('rooms', RoomViewSet)
router.register('reports', ReportViewSet)
router.register('reservations', ReservationViewSet)



urlpatterns = [
    path('', include(router.urls)),
]
