from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAccountViewSet, RoomViewSet, RoomTypeViewSet, RoomTypePriceViewSet, EmployeeViewSet, \
    PositionViewSet, SalaryHistoryViewSet, ContractViewSet, WorkScheduleViewSet, BookingViewSet, clients_in_room, \
    clients_from_city, free_rooms_count
from .views import (
    clients_per_room,
    rooms_per_floor,
    total_income_per_room,
    total_income,
)

router = DefaultRouter()
router.register('useraccounts', UserAccountViewSet)
router.register('rooms', RoomViewSet)
router.register('roomtypes', RoomTypeViewSet)
router.register('roomtypeprices', RoomTypePriceViewSet)
router.register('employees', EmployeeViewSet)
router.register('positions', PositionViewSet)
router.register('salaryhistories', SalaryHistoryViewSet)
router.register('contracts', ContractViewSet)
router.register('workschedules', WorkScheduleViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('clients-per-room/', clients_per_room, name='clients_per_room'),
    path('rooms-per-floor/', rooms_per_floor, name='rooms_per_floor'),
    path('total-income-per-room/', total_income_per_room, name='total_income_per_room'),
    path('total-income/', total_income, name='total_income'),
    path('clients-in-room/', clients_in_room, name='clients_in_room'),
    path('clients-from-city/', clients_from_city, name='clients_from_city'),
    path('free-rooms-count/', free_rooms_count, name='free_rooms_count'),
]
