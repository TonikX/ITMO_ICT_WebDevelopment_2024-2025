from django.urls import path

from hotel_app.views import FreeRoomsAPIView, ClientsFromCityAPIView, ReservationClientsAPIView, \
    EmployeeFromClientRoomAPIView, ClientByOtherClientAPIView, ReportAPIView, EmployeesAPIView, \
    EmployeeSchedulesAPIView, EmployeeScheduleUpdateView, ReservationDetailsView, \
    EmployeeDetailsAPIView, RoomsAPIView, RoomDetailsAPIView, ReservationsAPIView, ClientsAPIView

urlpatterns = [
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
    path('employees/schedule/<int:employee_id>/update', EmployeeScheduleUpdateView.as_view()),
    path('employees/<int:pk>', EmployeeDetailsAPIView.as_view())
]
