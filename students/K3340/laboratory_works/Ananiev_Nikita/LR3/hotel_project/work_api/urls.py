from django.urls import path
from .views import *


app_name = "work_api"

urlpatterns = [
    path('employees/<int:id>/', EmployeeAPIView.as_view(), name='get_employee'),
    path('employees/list/', EmployeeListAPIView.as_view(), name='get_employee_list'),
    path('employees/add/', EmployeeCreateAPIView.as_view(), name='add_employee'),
    path('positions/<int:id>/', PositionAPIView.as_view(), name='get_position'),
    path('positions/list/', PositionListAPIView.as_view(), name='get_position_list'),
    path('contracts/<int:id>/', ContractAPIView.as_view(), name='get_contract'),
    path('contracts/list/', ContractListAPIView.as_view(), name='get_contract_list'),
    path('contracts/add/', ContractCreateAPIView.as_view(), name='add_contract'),
    path('contracts/<int:id>/update/', ContractUpdateAPIView.as_view(), name='update_contract'),
    path('contracts/<int:id>/delete/', ContractDeleteAPIView.as_view(), name='delete_contract'),
    path('schedule/<int:id>/', ScheduleAPIView.as_view(), name='get_schedule'),
    path('schedule/list/', ScheduleListAPIView.as_view(), name='get_schedule_list'),
    path('schedule/add/', ScheduleCreateAPIView.as_view(), name='add_schedule'),
    path('schedule/<int:id>/update/', ScheduleUpdateAPIView.as_view(), name='update_schedule'),
    path('schedule/<int:id>/delete/', ScheduleDeleteAPIView.as_view(), name='delete_schedule'),
]