from django.urls import path, include
from .views import *

urlpatterns = [
    # Auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Standard CRUD
    path('airlines/', AirlinesAPIView.as_view(), name='airline_list'),
    path('airlines/<int:pk>/', AirlineAPIView.as_view(), name='airline_detail'),

    path('planes/', PlanesAPIView.as_view(), name='plane_list'),
    path('airlines/<int:airline_pk>/planes', PlanesAPIView.as_view(), name='planes_by_airline'),
    path('planes/<int:pk>/', PlaneAPIView.as_view(), name='plane_detail'),
    path('airlines/<int:airline_pk>/planes/<int:pk>/', PlaneAPIView.as_view(), name='plane_detail'),

    path('employees/', EmployeesAPIView.as_view(), name='employees_list'),
    path('airlines/<int:airline_pk>/employees', EmployeesAPIView.as_view(), name='employees_by_airline'),
    path('employees/<int:pk>/', EmployeeAPIView.as_view(), name='employee_detail'),
    path('airlines/<int:airline_pk>/employees/<int:pk>/', EmployeeAPIView.as_view(), name='employee_detail'),

    path('flights/', FlightsAPIView.as_view(), name='flight_list'),
    path('airlines/<int:airline_pk>/flights', FlightsAPIView.as_view(), name='flights_by_airline'),
    path('flights/<int:pk>/', FlightAPIView.as_view(), name='flight_detail'),
    path('airlines/<int:airline_pk>/flights/<int:pk>/', FlightAPIView.as_view(), name='flight_detail'),

    path('flights/<int:flight_pk>/seats/', SeatsAPIView.as_view(), name='flight_seats'),
    path('flights/<int:flight_id>/seat-availability/', FlightSeatAvailabilityAPIView.as_view(),
         name='flight_seat_availability'),
    path('flights/<int:pk>/available-seats/', AvailableSeatsAPIView.as_view(), name='available_seats'),
    path('flights/<int:flight_pk>/sell-seat/', SeatSellAPIView.as_view(), name='sell_seat'),

    path('routes/', RoutesAPIView.as_view(), name='route_list'),
    path('routes/<int:pk>/', RouteAPIView.as_view(), name='route_detail'),

    path('flights/<int:pk>/stops/', FlightTransitStopsAPIView.as_view(), name='flight_transit_stops'),

    path('crew-members/', CrewMembersAPIView.as_view(), name='crew_members'),

    path('crews/', CrewsAPIView.as_view(), name='crews'),

    path('maintenances/', MaintenancesAPIView.as_view(), name='maintenance_list'),
    path('maintenances/<int:pk>/', MaintenanceAPIView.as_view(), name='maintenance_detail'),


    # Statistics
    path('routes/<int:route_id>/most-frequent-plane/', MostFrequentPlaneAPIView.as_view(), name='most_frequent_plane'),
    path('routes/under-filled/', UnderFilledRoutesAPIView.as_view(), name='under_filled_routes'),

    path('planes/in-maintenance/', PlanesInMaintenanceAPIView.as_view(), name='planes_in_maintenance'),

    path('airlines/<int:airline_id>/employees-count/', AirlineEmployeesCountAPIView.as_view(),
         name='airline_employees_count'),

    path('airlines/<int:pk>/plane-statistics/', PlaneStatisticsAPIView.as_view(), name='plane_statistics'),

    path('flights/by-airport/<str:airport_code>/', FlightsByAirportAPIView.as_view(), name='flights_by_airport'),

    path('flights/with-transit-stops/', FlightsWithTransitStopsAPIView.as_view(), name='flights_with_transit_stops'),

]
