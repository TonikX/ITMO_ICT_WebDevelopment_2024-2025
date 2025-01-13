from django.urls import include, path
from rest_framework import routers
from .views import (
    BusTypeViewSet,
    BusViewSet,
    DriverViewSet,
    RouteViewSet,
    WorkShiftViewSet,
    DriversByRouteView,
    RouteStatsViewSet,
)

router = routers.DefaultRouter()
router.register(r'bus-types', BusTypeViewSet)
router.register(r'buses', BusViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'work-shifts', WorkShiftViewSet)
router.register(r'route-stats', RouteStatsViewSet, basename='route-stats')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
urlpatterns += [
    path('drivers/route/<int:route_id>/', DriversByRouteView.as_view(), name='drivers-by-route'),
]