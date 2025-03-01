from django.urls import path
from .views import *

app_name = "hostel_app"

urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='employee_list'),
    path('employees/<pk>', EmployeeDetail.as_view(), name='employee_retrieve'),
    path('rooms/', AvailableRoomsList.as_view(), name='room_list'),
    path('clients/', ClientList.as_view(), name='client_list'),
    path('clients/<pk>/', ClientDetail.as_view(), name='client_detail'),
    path('check-ins/', ClientRoomList.as_view(), name='check_in'),
    path('check-ins/<pk>/', ClientRoomDetail.as_view(), name='check_in_detail'),
    path('reports/', ReportList.as_view(), name='report_list'),
    path('floors/', FloorList.as_view(), name='floor_list'),
]
