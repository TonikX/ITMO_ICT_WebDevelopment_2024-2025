from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirlineViewSet, AircraftTypeViewSet, AirplaneViewSet, RouteViewSet,
    FlightViewSet, TransitStopViewSet, EmployeeViewSet, CrewViewSet,
    CrewEmployeeViewSet, FlightInstanceViewSet, MostCommonAircraftByRouteView, LowCapacityFlightsView,
    AvailableSeatsView, AircraftInRepairView, EmployeesCountView
)

router = DefaultRouter()
router.register('airlines', AirlineViewSet)
router.register('aircraft-types', AircraftTypeViewSet)
router.register('airplanes', AirplaneViewSet)
router.register('routes', RouteViewSet)
router.register('flights', FlightViewSet)
router.register('transit-stops', TransitStopViewSet)
router.register('employees', EmployeeViewSet)
router.register('crews', CrewViewSet)
router.register('crew-employees', CrewEmployeeViewSet)
router.register('flight-instances', FlightInstanceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('most-common-aircraft/', MostCommonAircraftByRouteView.as_view(), name='most-common-aircraft'),
    path('low-capacity-flights/', LowCapacityFlightsView.as_view(), name='low-capacity-flights'),
    path('available-seats/', AvailableSeatsView.as_view(), name='available-seats'),
    path('aircraft-in-repair/', AircraftInRepairView.as_view(), name='aircraft-in-repair'),
    path('employees-count/', EmployeesCountView.as_view(), name='employees-count'),
]

