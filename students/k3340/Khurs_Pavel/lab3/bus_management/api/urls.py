from django.urls import include, path
from rest_framework import routers
from .views import (
    BusTypeViewSet,
    BusViewSet,
    DriverViewSet,
    RouteViewSet,
    WorkShiftViewSet,
)

router = routers.DefaultRouter()
router.register(r'bus-types', BusTypeViewSet)
router.register(r'buses', BusViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'work-shifts', WorkShiftViewSet)

urlpatterns = [
    path('', include(router.urls)),
]