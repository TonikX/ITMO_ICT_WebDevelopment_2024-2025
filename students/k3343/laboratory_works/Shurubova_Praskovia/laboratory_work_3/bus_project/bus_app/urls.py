from django.urls import path
from .views import (
    DriverCreateAPIView, DriverListAPIView, DriverDetailAPIView,
    RouteCreateAPIView, RouteListAPIView, RouteDetailAPIView,
    BusCreateAPIView, BusListAPIView, BusDetailAPIView,
    DriverScheduleListAPIView, BusAssignmentListAPIView,
    MaintenanceListAPIView, DriverScheduleCreateAPIView, BusAssignmentCreateAPIView, MaintenanceCreateAPIView,
    RouteDeleteAPIView, DriverScheduleUpdateAPIView, MaintenanceUpdateAPIView, BusAssignmentUpdateAPIView,
    DriverUpdateAPIView, RouteUpdateAPIView, DriversForRouteAPIView, RouteScheduleAPIView, MissingBusesAPIView,
    DriverCountByClassAPIView, TotalRouteDurationAPIView
)


urlpatterns = [
    path('drivers/', DriverListAPIView.as_view(), name='driver-list'),
    path('drivers/create/', DriverCreateAPIView.as_view(), name='driver-create'),
    path('drivers/<int:pk>/', DriverDetailAPIView.as_view(), name='driver-detail'),
    path('routes/', RouteListAPIView.as_view(), name='route-list'),
    path('routes/create/', RouteCreateAPIView.as_view(), name='route-create'),
    path('routes/<int:pk>/', RouteDetailAPIView.as_view(), name='route-detail'),
    path('buses/', BusListAPIView.as_view(), name='bus-list'),
    path('buses/create/', BusCreateAPIView.as_view(), name='bus-create'),
    path('buses/<int:pk>/', BusDetailAPIView.as_view(), name='bus-detail'),
    path('driver-schedules/', DriverScheduleListAPIView.as_view(), name='driver-schedule-list'),
    path('bus-assignments/', BusAssignmentListAPIView.as_view(), name='bus-assignment-list'),
    path('maintenances/', MaintenanceListAPIView.as_view(), name='maintenance-list'),
    path("bus-assignments/create/", BusAssignmentCreateAPIView.as_view(), name="bus-assignment-create"),
    path("maintenance/create/", MaintenanceCreateAPIView.as_view(), name="maintenance-create"),
    path("driver-schedule/create/", DriverScheduleCreateAPIView.as_view(), name="driver-schedule-create"),
    path("routes/<int:pk>/delete/", RouteDeleteAPIView.as_view(), name="route-delete"),
    path("driver-schedules/<int:pk>/update/", DriverScheduleUpdateAPIView.as_view(), name="driver-schedule-update"),
    path("maintenance/<int:pk>/update/", MaintenanceUpdateAPIView.as_view(), name="maintenance-update"),
    path("bus-assignments/<int:pk>/update/", BusAssignmentUpdateAPIView.as_view(), name="bus-assignment-update"),
    path("drivers/<int:pk>/update/", DriverUpdateAPIView.as_view(), name="driver-update"),
    path("routes/<int:pk>/update/", RouteUpdateAPIView.as_view(), name="route-update"),
    path('drivers-for-route/', DriversForRouteAPIView.as_view(), name='drivers-for-route'),
    path('route-schedule/', RouteScheduleAPIView.as_view(), name='route-schedule'),
    path('missing-buses/', MissingBusesAPIView.as_view(), name='missing-buses'),
    path('driver-count-by-class/', DriverCountByClassAPIView.as_view(), name='driver-count-by-class'),
    path('total-duration/', TotalRouteDurationAPIView.as_view(), name='total-duration'),
]
