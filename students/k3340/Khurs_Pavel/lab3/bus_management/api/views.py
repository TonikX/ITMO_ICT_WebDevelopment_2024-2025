from rest_framework import viewsets
from .models import BusType, Bus, Driver, Route, WorkShift
from .serializers import (
    BusTypeSerializer,
    BusSerializer,
    DriverSerializer,
    RouteSerializer,
    WorkShiftSerializer,
)

class BusTypeViewSet(viewsets.ModelViewSet):
    queryset = BusType.objects.all()
    serializer_class = BusTypeSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class WorkShiftViewSet(viewsets.ModelViewSet):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer