import calendar
from datetime import datetime, date

from django.db import models
from django.core.exceptions import BadRequest
from django.utils import timezone
from django.db.models import Count, Sum, ExpressionWrapper, F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hotel_app.models import Client, Reservation, Employee, EmployeeSchedule, Room

from hotel_app.serializers import *

# from http import HTTPMethod
# from rest_framework.decorators import action

# @action(detail=False, methods=[HTTPMethod.GET])

class ReservationUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NestedReservationSerializer
    queryset = Reservation.objects.all()

class ClientsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        client = request.data.get('client')
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid(raise_exception=True):
            client_saved = serializer.save()
        return Response({"Success": "Client '{}' implemented succesfully.".format(client_saved.full_name)})
    
class ClientDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    lookup_field = 'id'


class ClientUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    lookup_field = 'id'


class RoomsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDetailsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'

class ReservationsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NestedReservationSerializer

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = NestedReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        admin_id = request.user.pk
        reservation = dict()
        room = request.data.get('room')
        client = request.data.get('client')
        arrival_date = request.data.get('arrival_date')
        departure_date = request.data.get('departure_date')
        reservation['admin'] = admin_id
        reservation['client'] = client
        reservation['arrival_date'] = arrival_date
        reservation['departure_date'] = departure_date
        reservation['room'] = room
        serializer = ReservationSerializer(data=reservation)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "reservation created"})
     

class EmployeesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        employee = request.data.get('employee')
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee_saved = serializer.save()
        return Response({"Congratulations!": "Employee '{}' added successfully.".format(employee_saved.full_name)})

class EmployeeDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"Something went wrong": "Employee '{}' is not added initially.".format(pk)})

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response({"Congratulations!": "Employee '{}' is deleted.".format(pk)})
        except Employee.DoesNotExist:
            return Response({"Something went wrong": "Employee '{}' is not added initially.".format(pk)})

class EmployeeSchedulesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeScheduleSerializer

    def get(self, request):
        employee_schedules = EmployeeSchedule.objects.all()
        serializer = EmployeeScheduleSerializer(employee_schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        employee_schedule = request.data
        serializer = EmployeeScheduleCreateSerializer(data=employee_schedule)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"Congratulations!": "Employee schedule implemented with success."})

class ReservationDetailsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get(self, request, id):
        try:
            reservation = Reservation.objects.get(pk=id)
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data)
        except Reservation.DoesNotExist:
            return Response({"Something went wrong": "Reservation with PK '{}' does not exist.".format(id)})

    def delete(self, request, id):
        try:
            reservation = Reservation.objects.get(pk=id)
            reservation.delete()
            return Response({"Congratulations!": "Reservation is deleted."})
        except Reservation.DoesNotExist:
            return Response({"Something went wrong": "Reservation with PK '{}' does not exist.".format(id)})


class EmployeeScheduleUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = EmployeeSchedule.objects.all()
    serializer_class = EmployeeScheduleUpdateSerializer
    lookup_field = 'id'


class FreeRoomsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"The number of free rooms: ": Reservation.objects.filter(departure_date__lte=datetime.now()).count()})


class ClientsFromCityAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city')
        return Response(
            {f"The number of clients from {city}: ": Client.objects.filter(city_from=city).count()})

class EmployeeFromClientRoomAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the employee who was cleaning the client's room",
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description="Target client's id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'day_of_week',
                openapi.IN_QUERY,
                description="The day of week the employee cleans the floor",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful search", schema=EmployeeSerializer),
        }
    )

    def get(self, request):
        client_id = request.query_params.get('client_id')
        day_of_week = request.query_params.get('day_of_week')
        reservations = Reservation.objects.filter(client_id=client_id)
        employees = []
        for reservations in reservations:
            floor = reservations.room.floor
            employee = EmployeeSchedule.objects.get(floor=floor, day_of_week=day_of_week).employee
            employees.append(employee)
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"Employees": serializer.data})

class ReservationClientsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get info about clients living in this room in the particular time.",
        manual_parameters=[
            openapi.Parameter(
                'room_id',
                openapi.IN_QUERY,
                description="target room id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful search", schema=EmployeeSerializer),
        }
    )

    def get(self, request):
        room_id = request.query_params.get('room_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        reservations = Reservation.objects.filter(
            room_id=room_id,
            arrival_date__lte=end_date,
            departure_date__gte=start_date
        )
        clients = []
        for reservation in reservations:
            clients.append(reservation.client)
        serializer = ClientSerializer(clients, many=True)
        return Response({"Clients": serializer.data})


class ClientByOtherClientAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get info about clients living in the hotel in the particular time with the target client.",
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description="target client id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End of period",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful search", schema=ClientSerializer),
        }
    )

    def get(self, request):
        client_id = request.query_params.get('client_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        target_client_reservations = Reservation.objects.filter(arrival_date__lte=end_date, #в конечную дату
                                                                departure_date__gte=start_date, client_id=client_id) #в начальную дату
        clients = []
        for target_client_reservations in target_client_reservations:
            reservations = Reservation.objects.filter(
                arrival_date=target_client_reservations.arrival_date,
                departure_date=target_client_reservations.departure_date
            ).exclude(id=target_client_reservations.id)
            for reservation in reservations:
                clients.append(reservation.client)

        serializer = ClientSerializer(clients, many=True)
        return Response({"Clients": serializer.data})

class ReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Receive the report for specific quarter.", #отчет по конкретному кварталу/промежутку времени
        manual_parameters=[
            openapi.Parameter(
                'quarter',
                openapi.IN_QUERY,
                description="The number of quarter",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="Successful search", schema=EmployeeSerializer),
        }
    )

    def get(self, request):
        print(request.data)
        quarter = int(request.query_params.get('quarter'))
        print(quarter)
        if not (1 <= quarter <= 4):
            raise BadRequest("Введите правильный номер квартала (от 1 до 4)")

        current_year = timezone.now().year 
        #создание логики кварталов
        quarter_start_month = 3 * (quarter - 1) + 1
        quarter_end_month = 3 * quarter

        quarter_start = date(
            year=current_year,
            month=quarter_start_month,
            day=1,
        )

        quarter_end = date(
            year=current_year,
            month=quarter_end_month,
            day=calendar.monthrange(current_year, quarter_end_month)[1],
        )

        report = {
            "clients_per_room": self._get_clients_per_room(quarter_start, quarter_end),
            "rooms_per_floor": self._get_rooms_per_floor(),
            "profit_per_room": self._get_profit_per_room(quarter_start, quarter_end),
            "total_profit": self._calculate_total_profit(quarter_start, quarter_end),
        }

        return Response(report)

    def _get_clients_per_room(self, quarter_start, quarter_end):
        return Reservation.objects.filter(arrival_date__lte=quarter_end, departure_date__gte=quarter_start).values(
            "room").annotate(count_of_clients=Count("client"))

    def _get_rooms_per_floor(self):
        return Room.objects.values("floor").annotate(rooms_count=Count("floor"))

    def _get_profit_per_room(self, quarter_start, quarter_end):
        return Reservation.objects.filter(arrival_date__lte=quarter_end, departure_date__gte=quarter_start).values(
            "room").annotate(profit=Sum("room__cost"))

    def _calculate_total_profit(self, quarter_start, quarter_end):
        return Reservation.objects.filter(
            arrival_date__lte=quarter_end,
            departure_date__gte=quarter_start
        ).aggregate(
            total_profit=Sum(ExpressionWrapper(F("room__cost"), output_field=models.IntegerField()))
        ).get("total_profit")

