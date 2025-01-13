# Ссылки

## Описание

Реализовать представления для приложения.

## Стек

- Python
- django
- restFramework
- djoser
- drf_yasg

## Листинг

### views.py:

### Представление главной страницы:
```python
from django.db.models import Count, Sum
from rest_framework import viewsets, status, generics
from django.db import models
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import BusType, Bus, Driver, Route, WorkShift
from rest_framework.response import Response
from .serializers import (
    BusTypeSerializer,
    BusSerializer,
    DriverSerializer,
    RouteSerializer,
    WorkShiftSerializer, RouteTimeSerializer,
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

    def get(self,request,*args,**kwargs):
        driver_id = kwargs.get('id')
        if driver_id:
            driver = self.get_queryset().filter(id=driver_id).first()
        serializer = self.get_serializer(driver)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class WorkShiftViewSet(viewsets.ModelViewSet):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer

class DriversByRouteView(generics.ListAPIView): #работает
    serializer_class = DriverSerializer

    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return Driver.objects.filter(workshift__route_id=route_id)


class RouteStatsViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteTimeSerializer  
        return RouteTimeSerializer  

    @action(detail=False, methods=['GET'])
    def total_duration(self, request):
        total_duration = self.queryset.aggregate(total_duration=Sum('duration'))['total_duration']
        return Response({'total_route_duration': total_duration})

    @action(detail=False, methods=['GET'])
    def driver_class_count(self, request):
        driver_classes = Driver.objects.values('driver_class').annotate(count=Count('id'))
        return Response(driver_classes)


```