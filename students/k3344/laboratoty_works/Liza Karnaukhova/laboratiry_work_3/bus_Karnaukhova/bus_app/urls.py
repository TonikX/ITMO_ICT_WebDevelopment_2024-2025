from django.urls import path
from .views import (
    BusDriversListAPIView, BusDriverCreateView, BusDriverDetailView,
    BusesListAPIView, BusCreateView, BusDetailView,
    RoutesListAPIView, RouteCreateView, RouteDetailView,
    WorkSchedulesListAPIView, WorkScheduleCreateView, WorkScheduleDetailView,
    DriversByRouteView, RouteTimingView, TotalRouteDurationView,
    AbsentBusesView, DriverCountByCategoryView, ReportView
)

urlpatterns = [
    # Водители
    path('drivers/', BusDriversListAPIView.as_view(), name='driver-list'),
    path('drivers/create/', BusDriverCreateView.as_view(), name='driver-create'),
    path('drivers/<str:passport>/', BusDriverDetailView.as_view(), name='driver-detail'),

    # Автобусы
    path('buses/', BusesListAPIView.as_view(), name='bus-list'),
    path('buses/create/', BusCreateView.as_view(), name='bus-create'),
    path('buses/<str:state_num>/', BusDetailView.as_view(), name='bus-detail'),

    # Маршруты
    path('routes/', RoutesListAPIView.as_view(), name='route-list'),
    path('routes/create/', RouteCreateView.as_view(), name='route-create'),
    path('routes/<str:route_num>/', RouteDetailView.as_view(), name='route-detail'),

    # Расписания
    path('work-schedules/', WorkSchedulesListAPIView.as_view(), name='work-schedule-list'),
    path('work-schedules/create/', WorkScheduleCreateView.as_view(), name='work-schedule-create'),
    path('work-schedules/<int:pk>/', WorkScheduleDetailView.as_view(), name='work-schedule-detail'),

    # Особые запросы
    path('drivers-by-route/<str:route_num>/', DriversByRouteView.as_view(), name='drivers-by-route'),
    path('route-timing/', RouteTimingView.as_view(), name='route-timing'),
    path('total-route-duration/', TotalRouteDurationView.as_view(), name='total-route-duration'),
    path('absent-buses/<str:date>/', AbsentBusesView.as_view(), name='absent-buses'),
    path('driver-count-by-category/', DriverCountByCategoryView.as_view(), name='driver-count-by-category'),
    path('fleet-report/', ReportView.as_view(), name='fleet-report'),
]