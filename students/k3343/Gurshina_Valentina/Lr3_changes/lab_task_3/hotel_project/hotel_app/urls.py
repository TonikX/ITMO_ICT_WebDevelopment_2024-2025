from django.urls import path, re_path

from hotel_app.views import FreeRoomsAPIView, ClientsFromCityAPIView, ReservationClientsAPIView, \
    EmployeeFromClientRoomAPIView, ClientByOtherClientAPIView, ReportAPIView, EmployeesAPIView, \
    EmployeeSchedulesAPIView, EmployeeScheduleUpdateView, ReservationDetailsView, \
    EmployeeDetailsAPIView, ReservationUpdateView, RoomsAPIView, RoomDetailsAPIView, ReservationsAPIView, ClientsAPIView, ClientDeleteView, ClientUpdateView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hotel API",
        default_version='v1',
        description="API documentation for Hotel management system",
        contact=openapi.Contact(email="contact_us@hotel.local"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('reservations/<int:pk>/update', ReservationUpdateView.as_view()),
    path('rooms/free', FreeRoomsAPIView.as_view()),
    path('rooms', RoomsAPIView.as_view()),
    path('rooms/<int:id>', RoomDetailsAPIView.as_view()),
    path('clients/city', ClientsFromCityAPIView.as_view()),
    path('clients', ClientsAPIView.as_view()),
    path('reservations', ReservationsAPIView.as_view()),
    path('reservations/room_period', ReservationClientsAPIView.as_view()),
    path('reservations/<int:id>', ReservationDetailsView.as_view()),
    path('reservations/client_period', ClientByOtherClientAPIView.as_view()),
    path('report', ReportAPIView.as_view()),
    path('employees/schedule_client', EmployeeFromClientRoomAPIView.as_view()),
    path('employees', EmployeesAPIView.as_view()),
    path('employees/schedule', EmployeeSchedulesAPIView.as_view()),
    path('employees/schedule/<int:id>/update', EmployeeScheduleUpdateView.as_view()),
    path('employees/<int:pk>', EmployeeDetailsAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('clients/<int:id>/delete', ClientDeleteView.as_view()),
    path('clients/<int:id>/update', ClientUpdateView.as_view()),

]
