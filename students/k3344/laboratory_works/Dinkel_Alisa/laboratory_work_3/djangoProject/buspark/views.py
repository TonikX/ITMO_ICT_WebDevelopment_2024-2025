from rest_framework import generics
from .models import BusCategory, Bus, Driver, Route, Shift
from .serializers import BusCategorySerializer, BusSerializer, DriverSerializer, RouteSerializer, ShiftSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Avg


# Типы автобусов
class BusCategoryListCreateView(generics.ListCreateAPIView):  # получить список всех объектов и создать новый объект
    queryset = BusCategory.objects.all()
    serializer_class = BusCategorySerializer


class BusCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):  # получить конкретный объект, обновить его или удалить
    queryset = BusCategory.objects.all()
    serializer_class = BusCategorySerializer


# Автобусы
class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class BusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


# Водители
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


# Маршруты
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


# Смены
class ShiftListCreateView(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class ShiftRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


# Список водителей на маршруте с их графиком работы
class DriversOnRouteView(APIView):
    def get(self, request, route_id):
        shifts = Shift.objects.filter(route_id=route_id).select_related('driver')
        data = [
            {
                "driver": shift.driver.full_name,
                "shift_date": shift.shift_date,
                "start_time": shift.start_time,
                "end_time": shift.end_time
            }
            for shift in shifts
        ]
        return Response(data)


# Общая протяженность всех маршрутов
class TotalRouteDistanceView(APIView):
    def get(self, request):
        total_distance = Route.objects.aggregate(total=Sum('duration_minutes'))['total'] or 0
        return Response({"total_route_duration": total_distance})


# Автобусы, не вышедшие на линию
class InactiveBusesView(APIView):
    def get(self, request, date):
        breakdown_shifts = Shift.objects.filter(shift_date=date, status="Breakdown")
        data = [
            {
                "route": shift.route.route_number,
                "bus": shift.bus.registration_number,
                "driver": shift.driver.full_name,
                "status": shift.status,
                "reason": shift.reason
            }
            for shift in breakdown_shifts
        ]
        return Response(data)


# Водители, не вышедшие на линию
class InactiveDriversView(APIView):
    def get(self, request, date):
        no_driver_shifts = Shift.objects.filter(shift_date=date, status="No Driver")
        data = [
            {
                "route": shift.route.route_number,
                "driver": shift.driver.full_name,
                "bus": shift.bus.registration_number,
                "status": shift.status,
                "reason": shift.reason
            }
            for shift in no_driver_shifts
        ]
        return Response(data)


# Время начала и окончания движения автобусов на маршрутах
class RouteScheduleView(APIView):
    def get(self, request):
        routes = Route.objects.all()
        data = []
        for route in routes:
            shifts = Shift.objects.filter(route=route).order_by("start_time")
            if shifts.exists():
                data.append({
                    "route": route.route_number,
                    "first_bus_start": shifts.first().start_time,
                    "last_bus_end": shifts.last().end_time
                })
        return Response(data)


# Количество водителей каждого класса
class DriverCategoryCountView(APIView):
    def get(self, request):
        driver_counts = Driver.objects.values("driver_class").annotate(count=Count("id"))
        return Response({"drivers_by_category": list(driver_counts)})


# Отчет о состоянии автопарка, включая количество автобусов по типам, маршруты и водителей.
class ReportView(APIView):
    def get(self, request):
        # Сгруппировать автобусы по категориям и посчитать количество автобусов, маршрутов и водителей
        bus_types = Bus.objects.values('category__name').annotate(
            bus_count=Count('id'),  # Количество автобусов
            route_count=Count('shift__route', distinct=True),  # Количество уникальных маршрутов, обслуживаемых автобусами
            driver_count=Count('shift__driver', distinct=True),  # Количество уникальных водителей, обслуживающих эти автобусы
        )

        # Суммарная протяженность всех маршрутов
        total_duration = Route.objects.aggregate(total_duration=Sum('duration_minutes'))['total_duration']

        # Статистика по водителям: средний стаж и общее количество водителей
        driver_stats = Driver.objects.aggregate(
            avg_experience=Avg('experience'),  # Средний стаж водителей
            total_count=Count('id')  # Общее количество водителей
        )

        # Получаем список маршрутов с их характеристиками, включая автобусы и водителей
        route_details = Route.objects.annotate(
            bus_count=Count('shift__bus', distinct=True),  # Количество автобусов на маршруте
            driver_count=Count('shift__driver', distinct=True)  # Количество водителей на маршруте
        ).values('route_number', 'start_point', 'end_point', 'bus_count', 'driver_count', 'duration_minutes')

        # Формируем отчет
        report = {
            'bus_types': list(bus_types),  # Сгруппированные данные по типам автобусов
            'total_route_duration': total_duration,  # Суммарная длительность маршрутов
            'driver_stats': driver_stats,  # Статистика по водителям
            'route_details': list(route_details)  # Детали по маршрутам
        }

        # Возвращаем отчет в виде JSON
        return Response(report)
