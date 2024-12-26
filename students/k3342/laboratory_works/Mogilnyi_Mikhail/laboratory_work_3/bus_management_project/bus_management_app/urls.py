from django.urls import path, include

from bus_management_app.views import BusesListAPIView, RoutesListAPIView, DriversListAPIView, SchedulesListAPIView, \
    DriversByRouteView, RouteTimingView, TotalRouteDistanceView, AbsentBusesView, DriverCountByClassView, \
    FleetReportView, BusesDestroyView, BusesCreateView, RoutesCreateView, RoutesDestroyView, ScheduleCreateView, \
    ScheduleUpdateView, ScheduleDeleteView, DriverDeleteView, DriverCreateView, DriverDetailView, DriverUpdateView

urlpatterns = [
    # Для авторизации
    path('auth/', include("djoser.urls")),

    path('auth/', include("djoser.urls.authtoken")),

    # Эндпоинты Автобус
    path('buses', BusesListAPIView.as_view()),
    path('add-bus/', BusesCreateView.as_view()),
    path('delete-bus/<str:registration_number>/', BusesDestroyView.as_view()),

    # Эндпоинты Маршрут
    path('routes', RoutesListAPIView.as_view()),
    path('add-route', RoutesCreateView.as_view()),
    path('delete-route/<str:route_number>/', RoutesDestroyView.as_view()),

    # Эндопинты Водитель
    path('drivers', DriversListAPIView.as_view()),
    path('drivers/create/', DriverCreateView.as_view()),
    path('drivers/<str:passport_number>/', DriverDetailView.as_view()),
    path('drivers/<str:passport_number>/update/', DriverUpdateView.as_view()),
    path('drivers/<str:passport_number>/delete/', DriverDeleteView.as_view()),

    # Эндпоинты Расписание
    path('schedules', SchedulesListAPIView.as_view()),
    path('create-schedule/', ScheduleCreateView.as_view()),
    path('update-schedule/<int:pk>/', ScheduleUpdateView.as_view()),
    path('delete-schedule/<int:pk>/', ScheduleDeleteView.as_view()),

    path('drivers-by-route/<str:route_number>/', DriversByRouteView.as_view()),
    path('route-timing/', RouteTimingView.as_view()),
    path('total-route-distance/', TotalRouteDistanceView.as_view()),
    path('absent-buses/<str:date>/', AbsentBusesView.as_view()),
    path('driver-count-by-class/', DriverCountByClassView.as_view()),
    path('fleet-report/', FleetReportView.as_view()),
]