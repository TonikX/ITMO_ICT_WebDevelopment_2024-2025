from django.urls import path
from .views import *

app_name = "hotel_app"

urlpatterns = [
    # Rooms
    path('rooms/', RoomsAPIView.as_view(), name='rooms-list'),
    path('rooms/<int:room_id>/', RoomAPIView.as_view(), name='room-actions'),

    # Employees
    path('employees/', EmployeesAPIView.as_view(), name='employees-list'),
    path('employees/<int:employee_id>/', EmployeeAPIView.as_view(), name='employee-actions'),

    # Clients
    path('clients/', ClientsAPIView.as_view(), name='client-list'),
    path('clients/<int:client_id>/', ClientAPIView.as_view(), name='employee-actions'),

    # Bookings
    path('bookings/', BookingsAPIView.as_view(), name='bookings-list'),
    path('bookings/<int:booking_id>/', BookingAPIView.as_view(), name='booking-actions'),

    # Cleanings
    path('cleanings/', CleaningsAPIView.as_view(), name='cleanings-list'),
    path('cleanings/<int:cleaning_id>/', CleaningAPIView.as_view(), name='cleaning-actions'),

    # Additional tasks
    path('clients-in-room/<int:room_id>/<str:start_date>/<str:end_date>/',
         ClientsInRoomView.as_view(), name='clients-in-room'),
    path('clients-from-city/<str:origin_city>/', ClientsFromCityView.as_view(),
         name='clients-from-city-count'),
    path('cleaning-employees/<int:client_id>/<str:week_day>/',
         EmployeesWhoCleanedView.as_view(), name='cleaning-employees'),
    path('free-rooms/<str:start_date>/<str:end_date>/', FreeRoomsView.as_view(),
         name='free-rooms-count'),
    path('clients-while-client/<int:request_client_id>/', ClientsWhileClientView.as_view(),
         name='client-while-client'),

    # Quarter report
    path('report/<int:requested_quarter>/', QuarterReportAPIView.as_view(), name='report')
]
