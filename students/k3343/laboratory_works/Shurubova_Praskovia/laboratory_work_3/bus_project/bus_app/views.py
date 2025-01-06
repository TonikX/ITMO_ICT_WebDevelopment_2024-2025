from django.db.models import Sum
from rest_framework import serializers, status
from requests import Response
from rest_framework.response import Response
from rest_framework import generics
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Driver, Route, Bus, DriverSchedule, BusAssignment, Maintenance
from .serializers import (
    DriverSerializer, RouteSerializer, BusSerializer,
    DriverScheduleSerializer, BusAssignmentSerializer, MaintenanceSerializer
)


class DriverCreateAPIView(generics.CreateAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = [IsAuthenticated]


class DriverListAPIView(generics.ListAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.prefetch_related('routes').all()


class DriverDetailAPIView(generics.RetrieveAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.prefetch_related('routes').all()


class RouteCreateAPIView(generics.CreateAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteListAPIView(generics.ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class BusCreateAPIView(generics.CreateAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class BusListAPIView(generics.ListAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class BusDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class DriverScheduleListAPIView(generics.ListAPIView):
    serializer_class = DriverScheduleSerializer
    queryset = DriverSchedule.objects.select_related('driver', 'bus', 'route').all()


class BusAssignmentListAPIView(generics.ListAPIView):
    serializer_class = BusAssignmentSerializer
    queryset = BusAssignment.objects.select_related('bus', 'route').all()


class MaintenanceListAPIView(generics.ListAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.select_related('bus').all()


class DriverScheduleCreateAPIView(generics.CreateAPIView):
    serializer_class = DriverScheduleSerializer
    queryset = DriverSchedule.objects.select_related('driver', 'bus', 'route').all()


class BusAssignmentCreateAPIView(generics.CreateAPIView):
    serializer_class = BusAssignmentSerializer
    queryset = BusAssignment.objects.select_related('bus', 'route').all()


class MaintenanceCreateAPIView(generics.CreateAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.select_related('bus').all()


class RouteDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class DriverScheduleUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DriverScheduleSerializer
    queryset = DriverSchedule.objects.select_related('driver', 'bus', 'route').all()


class MaintenanceUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MaintenanceSerializer
    queryset = Maintenance.objects.select_related('bus').all()


class BusAssignmentUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = BusAssignmentSerializer
    queryset = BusAssignment.objects.select_related('bus', 'route').all()


class DriverUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.prefetch_related('routes').all()


class RouteUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_num', 'start_point', 'end_point', 'start_time', 'end_time']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['name', 'surname']


class DriverScheduleSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = DriverSchedule
        fields = ['id', 'work_date', 'shift_start', 'shift_end', 'driver', 'bus', 'route']


class DriversForRouteAPIView(generics.ListAPIView):
    "Список водителей, работающих на определенном маршруте с указанием графика их работы"

    serializer_class = DriverScheduleSerializer

    def get_queryset(self):
        route_num = self.request.query_params.get('route_num')
        return DriverSchedule.objects.filter(route__route_num=route_num).select_related('driver', 'route')


class RouteScheduleAPIView(generics.ListAPIView):
    "Когда начинается и заканчивается движение автобусов на каждом маршруте?"
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class MissingBusesAPIView(APIView):
    def get(self, request):
        date = self.request.query_params.get('date')
        if not date:
            return Response({"error": "Пожалуйста, укажите дату."}, status=status.HTTP_400_BAD_REQUEST)

        scheduled_buses = DriverSchedule.objects.filter(work_date=date).values_list('bus_id', flat=True)

        unscheduled_buses = Bus.objects.exclude(id__in=scheduled_buses).prefetch_related('maintenance_set')

        data = []
        for bus in unscheduled_buses:
            reason = None
            if bus.status == Bus.BusStatus.IN_REPAIR:
                maintenance = bus.maintenance_set.filter(maintenance_date=date).first()
                reason = maintenance.reason if maintenance else "Не указана"
            else:
                reason = "Нет водителя"
            data.append({"bus": bus.registration_num, "reason": reason})

        return Response(data)


class DriverCountByClassAPIView(APIView):
    "Сколько водителей каждого класса работает в автопарке?"
    def get(self, request):
        driver_counts = Driver.objects.values('driver_class').annotate(count=models.Count('id'))
        return Response({"driver_counts": driver_counts})


class TotalRouteDurationAPIView(APIView):
    "Какова общая протяженность маршрутов, обслуживаемых автопарком?"

    def get(self, request, *args, **kwargs):
        total_duration = Route.objects.aggregate(total=Sum('duration'))['total'] or 0
        return Response({"total_duration": total_duration})