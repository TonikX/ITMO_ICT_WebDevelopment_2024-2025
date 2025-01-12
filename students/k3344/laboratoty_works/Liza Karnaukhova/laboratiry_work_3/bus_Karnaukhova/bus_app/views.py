from django.db.models import Count, Sum, Avg
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BusDriver, Bus, Route, WorkSchedule
from .serializers import BusDriverSerializer, BusSerializer, RouteSerializer, WorkScheduleSerializer

class BusDriversListAPIView(generics.ListAPIView):
    serializer_class = BusDriverSerializer
    queryset = BusDriver.objects.all()


class BusDriverCreateView(generics.CreateAPIView):
    serializer_class = BusDriverSerializer
    queryset = BusDriver.objects.all()


class BusDriverDetailView(generics.RetrieveAPIView):
    serializer_class = BusDriverSerializer
    queryset = BusDriver.objects.all()
    lookup_field = 'passport'

class BusesListAPIView(generics.ListAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class BusCreateView(generics.CreateAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class BusDetailView(generics.RetrieveAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()
    lookup_field = 'state_num'


class RoutesListAPIView(generics.ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteCreateView(generics.CreateAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class RouteDetailView(generics.RetrieveAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    lookup_field = 'route_num'


class WorkSchedulesListAPIView(generics.ListAPIView):
    serializer_class = WorkScheduleSerializer
    queryset = WorkSchedule.objects.all()


class WorkScheduleCreateView(generics.CreateAPIView):
    serializer_class = WorkScheduleSerializer
    queryset = WorkSchedule.objects.all()


class WorkScheduleDetailView(generics.RetrieveAPIView):
    serializer_class = WorkScheduleSerializer
    queryset = WorkSchedule.objects.all()


# Особые запросы
class DriversByRouteView(APIView):
    """Список водителей, работающих на определенном маршруте с указанием графика их работы?"""
    def get(self, request, route_num):
        schedules = WorkSchedule.objects.filter(route__route_num=route_num).select_related('driver', 'route')
        serialized_data = WorkScheduleSerializer(schedules, many=True).data
        return Response(serialized_data)


class RouteTimingView(APIView):
    """Когда начинается и заканчивается движение автобусов на каждом маршруте?"""
    def get(self, request):
        routes = Route.objects.all()
        data = routes.values('route_num', 'start_time', 'end_time')
        return Response(data)


class TotalRouteDurationView(APIView):
    """Какова общая протяженность маршрутов, обслуживаемых автопарком?"""
    def get(self, request):
        total_duration = Route.objects.aggregate(total_duration=Sum('duration'))
        return Response({'total_duration': total_duration['total_duration']})


class AbsentBusesView(APIView):
    """Какие автобусы не вышли на линию в заданный день и по какой причине?"""
    def get(self, request, date):
        absent_schedules = WorkSchedule.objects.filter(date=date, status=WorkSchedule.Status.INACTIVE)
        serialized_data = WorkScheduleSerializer(absent_schedules, many=True).data
        return Response(serialized_data)


class DriverCountByCategoryView(APIView):
    """Сколько водителей каждого класса работает в автопарке?"""
    def get(self, request):
        driver_counts = BusDriver.objects.values('driver_category').annotate(count=Count('id'))
        return Response(driver_counts)


class ReportView(APIView):
    """Каково общее состояние автопарка, включая количество автобусов по типам, количество маршрутов, которые они обслуживают, количество водителей, а также средний стаж работы водителей?"""
    def get(self, request):
        bus_types = Bus.objects.values('bus_type').annotate(
            bus_count=Count('id'),
            route_count=Count('schedules__route', distinct=True),
            driver_count=Count('schedules__driver', distinct=True),
        )
        total_duration = Route.objects.aggregate(total_duration=Sum('duration'))
        driver_stats = BusDriver.objects.aggregate(
            avg_experience=Avg('experience'), total_count=Count('id')
        )
        report = {
            'bus_types': list(bus_types),
            'total_route_duration': total_duration['total_duration'],
            'driver_stats': driver_stats,
        }
        return Response(report)

