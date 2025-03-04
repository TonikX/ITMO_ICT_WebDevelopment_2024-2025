from rest_framework import generics
from rest_framework.response import Response
from datetime import date

from rest_framework.views import APIView

from .models import *
from .serializers import EmployeeSerializer, RoomSerializer, ClientSerializer, ClientRoomSerializer


class EmployeeList(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.prefetch_related(
            'cleaning_assignments__floor_schedule__floor'
        ).all()


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class AvailableRoomsList(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        count_of_clients = int(self.request.query_params.get('count_of_clients', 1))
        free_rooms = Room.get_free_rooms()
        available_rooms = [
            room for room in free_rooms if self.is_room_available_for_clients(room, count_of_clients)
        ]
        return available_rooms

    @classmethod
    def is_room_available_for_clients(cls, room, count_of_clients):
        max_capacity = {
            "single": 1,
            "double": 2,
            "triple": 3,
        }.get(room.room_type, 1)

        return count_of_clients <= max_capacity

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClientList(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientRoomList(generics.ListCreateAPIView):
    serializer_class = ClientRoomSerializer
    queryset = ClientRoom.objects.all()


class ClientRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientRoomSerializer
    queryset = ClientRoom.objects.all()


class ReportList(APIView):
    @classmethod
    def get(cls, request):
        quarter_param = request.query_params.get('quarter')
        if quarter_param not in ['1', '2', '3', '4']:
            return Response({"error": "Параметр quarter должен быть 1, 2, 3 или 4."}, status=400)

        quarter = int(quarter_param)
        current_year = date.today().year

        if quarter == 1:
            quarter_start = date(current_year, 1, 1)
            quarter_end = date(current_year, 3, 31)
        elif quarter == 2:
            quarter_start = date(current_year, 4, 1)
            quarter_end = date(current_year, 6, 30)
        elif quarter == 3:
            quarter_start = date(current_year, 7, 1)
            quarter_end = date(current_year, 9, 30)
        elif quarter == 4:
            quarter_start = date(current_year, 10, 1)
            quarter_end = date(current_year, 12, 31)

        client_rooms = ClientRoom.objects.filter(
            check_in_date__lte=quarter_end,
            check_out_date__gte=quarter_start,
            check_out_date__isnull=False
        ).select_related('room')

        room_stats = {}
        total_income = 0

        for cr in client_rooms:
            effective_start = max(cr.check_in_date, quarter_start)
            effective_end = min(cr.check_out_date, quarter_end)
            days = (effective_end - effective_start).days
            if days < 0:
                days = 0
            income = cr.room.price_per_day * days
            room_id = cr.room.id
            if room_id not in room_stats:
                room_stats[room_id] = {
                    "room_number": cr.room.number,
                    "client_count": 0,
                    "income": 0
                }
            room_stats[room_id]["client_count"] += cr.count_of_clients
            room_stats[room_id]["income"] += income
            total_income += income

        rooms_report = list(room_stats.values())
        report = {
            "quarter": quarter,
            "year": current_year,
            "rooms": rooms_report,
            "total_income": total_income
        }
        return Response(report)
