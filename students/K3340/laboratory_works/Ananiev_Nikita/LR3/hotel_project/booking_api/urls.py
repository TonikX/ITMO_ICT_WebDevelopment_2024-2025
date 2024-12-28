from django.urls import path
from .views import *


app_name = "booking_api"

urlpatterns = [
    path('bookings/<int:id>/', BookingAPIView.as_view(), name='get_booking'),
    path('bookings/list/', BookingListAPIView.as_view(), name='get_booking_list'),
    path('bookings/add/', BookingCreateAPIView.as_view(), name='add_booking'),
    path('bookings/<int:id>/update/', BookingUpdateAPIView.as_view(), name='update_booking'),
    path('bookings/<int:id>/delete/', BookingDeleteAPIView.as_view(), name='delete_booking'),
]