from django.urls import path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v2',
      description="Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="hardbeat34@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=([permissions.AllowAny]),
)

app_name = "hotel_app"

urlpatterns = [
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('rooms/', RoomsAPIView.as_view(), name='rooms-list'),
    path('rooms/<int:room_id>/', RoomAPIView.as_view(), name='room-actions'),

    path('employees/', EmployeesAPIView.as_view(), name='employees-list'),
    path('employees/<int:employee_id>/', EmployeeAPIView.as_view(), name='employee-actions'),

    path('clients/', ClientsAPIView.as_view(), name='client-list'),
    path('clients/<int:client_id>/', ClientAPIView.as_view(), name='employee-actions'),

    path('bookings/', BookingsAPIView.as_view(), name='bookings-list'),
    path('bookings/<int:booking_id>/', BookingAPIView.as_view(), name='booking-actions'),

    path('cleanings/', CleaningsAPIView.as_view(), name='cleanings-list'),
    path('cleanings/<int:cleaning_id>/', CleaningAPIView.as_view(), name='cleaning-actions'),


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

]
