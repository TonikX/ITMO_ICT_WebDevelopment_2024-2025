from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, ClientViewSet, StaffViewSet, StayViewSet,
    CleaningScheduleViewSet, CleaningExecutionViewSet
)

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'stays', StayViewSet)
router.register(r'cleaning-schedules', CleaningScheduleViewSet)
router.register(r'cleaning-executions', CleaningExecutionViewSet)



urlpatterns = router.urls