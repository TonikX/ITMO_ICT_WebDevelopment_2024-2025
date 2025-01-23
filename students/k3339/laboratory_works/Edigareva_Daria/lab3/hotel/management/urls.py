from django.urls import path
from .views import (
    RoomListCreateAPIView, RoomDetailAPIView,
    ClientListCreateAPIView, ClientDetailAPIView,
    BookingListCreateAPIView, BookingDetailAPIView,
    StaffListCreateAPIView, StaffDetailAPIView,
    CleaningScheduleListCreateAPIView, CleaningScheduleDetailAPIView,
    CleaningConfirmationListCreateAPIView, CleaningConfirmationDetailAPIView
)

urlpatterns = [
    # Rooms
    path('rooms/', RoomListCreateAPIView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),

    path('clients/', ClientListCreateAPIView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),

    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),

    path('staff/', StaffListCreateAPIView.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffDetailAPIView.as_view(), name='staff-detail'),

    path('cleaning-schedules/', CleaningScheduleListCreateAPIView.as_view(), name='cleaning-schedule-list'),
    path('cleaning-schedules/<int:pk>/', CleaningScheduleDetailAPIView.as_view(), name='cleaning-schedule-detail'),

    path('cleaning-confirmations/', CleaningConfirmationListCreateAPIView.as_view(), name='cleaning-confirmation-list'),
    path('cleaning-confirmations/<int:pk>/', CleaningConfirmationDetailAPIView.as_view(), name='cleaning-confirmation-detail'),
]
