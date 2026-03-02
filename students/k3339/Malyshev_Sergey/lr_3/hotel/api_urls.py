

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hotels.views import QuarterReportView


from hotels.views import (
    RoomTypeViewSet,
    RoomViewSet,
    GuestViewSet,
    BookingViewSet,
    EmployeeViewSet,
    CleaningAssignmentViewSet,
)

router = DefaultRouter()
router.register(r'room-types', RoomTypeViewSet, basename='roomtype')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'guests', GuestViewSet, basename='guest')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'cleaning-assignments', CleaningAssignmentViewSet, basename='cleaningassignment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reports/quarter/', QuarterReportView.as_view(), name='quarter-report'),  # ← добавь эту строку
]