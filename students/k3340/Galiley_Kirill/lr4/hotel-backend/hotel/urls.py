from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='room-detail'),
    path('clients/', views.ClientList.as_view(), name='client-list'),
    path('stays/', views.StayList.as_view(), name='stay-list'),
    path('stays/<int:pk>/', views.StayDetail.as_view(), name='stay-detail'),
    path('staff/', views.StaffList.as_view(), name='staff-list'),
    path('schedules/', views.CleaningScheduleList.as_view(), name='schedule-list'),
    path('queries/clients-in-room/', views.ClientsInRoomView.as_view(), name='clients-in-room'),
    path('queries/clients-from-city/', views.ClientsFromCityView.as_view(), name='clients-from-city'),
    path('queries/staff-for-client/', views.StaffForClientDayView.as_view(), name='staff-for-client'),
    path('queries/free-rooms/', views.FreeRoomsView.as_view(), name='free-rooms'),
    path('report/quarter/<int:quarter>/', views.QuarterlyReportView.as_view(), name='quarterly-report'),
]
